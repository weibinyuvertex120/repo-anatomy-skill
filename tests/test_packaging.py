#!/usr/bin/env python3
"""Regression tests for safe Skill package construction."""

from __future__ import annotations

import hashlib
import importlib.util
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/package_skills.py"
SPEC = importlib.util.spec_from_file_location("package_skills", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load package script: {SCRIPT}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="skill-package-tests-") as temporary:
        temp_root = Path(temporary)
        skill_root = temp_root / "skill"
        outside = temp_root / "outside.txt"
        skill_root.mkdir()
        outside.write_text("outside marker", encoding="utf-8")
        (skill_root / "SKILL.md").write_text("---\nname: fixture\n---\n", encoding="utf-8")
        (skill_root / "references").mkdir()
        (skill_root / "references" / "outside.txt").symlink_to(outside)
        try:
            MODULE.collect_files(skill_root)
        except MODULE.PackageError as exc:
            if "symlink is not allowed" not in str(exc):
                raise AssertionError(f"unexpected rejection: {exc}") from exc
            print("PASS rejects-external-symlink")
        else:
            raise AssertionError("external symlink must be rejected")

        output = temp_root / "packages"
        rebuilt_output = temp_root / "rebuilt-packages"
        expected = (
            ("workspace-file-maintainer", "0.1.0", 5),
            ("research-material-writer", "0.2.0-preview.1", 9),
        )
        release_assets: list[Path] = []
        rebuilt_assets: list[Path] = []
        for skill_name, expected_version, expected_count in expected:
            for variant in MODULE.VARIANTS:
                archive, manifest = MODULE.package_skill(skill_name, output, variant)
                manifest_path = archive.with_suffix(".manifest.json")
                manifest_path.write_text(MODULE.json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                release_assets.extend((archive, manifest_path))
                if manifest["version"] != expected_version:
                    raise AssertionError(f"{skill_name}: unexpected version {manifest['version']}")
                if manifest["variant"] != variant:
                    raise AssertionError(f"{skill_name}: unexpected variant {manifest['variant']}")
                with zipfile.ZipFile(archive) as package:
                    infos = package.infolist()
                    names = [info.filename for info in infos]
                    skill_md = package.read(f"{skill_name}/SKILL.md").decode("utf-8")
                    if len(names) != expected_count:
                        raise AssertionError(f"{skill_name}: expected {expected_count} files, got {len(names)}")
                    if any(name.startswith("../") or "/../" in name for name in names):
                        raise AssertionError(f"{skill_name}: archive contains traversal path")
                    if any(info.date_time != MODULE.ZIP_TIMESTAMP for info in infos):
                        raise AssertionError(f"{skill_name}: archive contains variable timestamps")
                    if any(info.create_system != 3 or info.external_attr >> 16 != MODULE.ZIP_FILE_MODE for info in infos):
                        raise AssertionError(f"{skill_name}: archive contains variable file metadata")
                    if variant == "workbuddy" and "agent_created: true" not in skill_md:
                        raise AssertionError(f"{skill_name}: WorkBuddy field missing")
                    if variant == "open-spec" and "agent_created:" in skill_md:
                        raise AssertionError(f"{skill_name}: host field leaked into open-spec package")
                rebuilt_archive, rebuilt_manifest = MODULE.package_skill(skill_name, rebuilt_output, variant)
                rebuilt_manifest_path = rebuilt_archive.with_suffix(".manifest.json")
                rebuilt_manifest_path.write_text(
                    MODULE.json.dumps(rebuilt_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
                )
                rebuilt_assets.extend((rebuilt_archive, rebuilt_manifest_path))
                if archive.read_bytes() != rebuilt_archive.read_bytes():
                    raise AssertionError(f"{skill_name}: repeated build changed ZIP bytes")
                if manifest != rebuilt_manifest:
                    raise AssertionError(f"{skill_name}: repeated build changed manifest")
                print(f"PASS packages-{skill_name}-{variant}")
                print(f"PASS reproducible-{skill_name}-{variant}")

        checksum_path = MODULE.write_checksum_file(output, release_assets)
        rebuilt_checksum_path = MODULE.write_checksum_file(rebuilt_output, rebuilt_assets)
        expected_asset_names = sorted(path.name for path in release_assets)
        checksum_lines = checksum_path.read_text(encoding="utf-8").splitlines()
        if len(checksum_lines) != 8:
            raise AssertionError(f"SHA256SUMS: expected 8 entries, got {len(checksum_lines)}")
        actual_asset_names: list[str] = []
        for line in checksum_lines:
            digest, name = line.split("  ", 1)
            asset = output / name
            if Path(name).name != name:
                raise AssertionError(f"SHA256SUMS: non-flat asset name {name}")
            if digest != hashlib.sha256(asset.read_bytes()).hexdigest():
                raise AssertionError(f"SHA256SUMS: digest mismatch for {name}")
            actual_asset_names.append(name)
        if actual_asset_names != expected_asset_names:
            raise AssertionError("SHA256SUMS: entries are incomplete or not sorted")
        if checksum_path.read_bytes() != rebuilt_checksum_path.read_bytes():
            raise AssertionError("SHA256SUMS: repeated build changed aggregate checksums")
        print("PASS aggregate-sha256sums")
    print("Packaging regression tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
