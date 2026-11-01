#!/usr/bin/env python3
"""Regression tests for the deterministic Copilot read-only adapter package."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/package_copilot_adapter.py"
SPEC = importlib.util.spec_from_file_location("package_copilot_adapter", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load Copilot package script: {SCRIPT}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="copilot-adapter-tests-") as temporary:
        root = Path(temporary)
        output = root / "output"
        rebuilt = root / "rebuilt"

        archive, manifest = MODULE.package_adapter(output)
        rebuilt_archive, rebuilt_manifest = MODULE.package_adapter(rebuilt)
        if archive.read_bytes() != rebuilt_archive.read_bytes():
            raise AssertionError("repeated Copilot build changed ZIP bytes")
        if manifest != rebuilt_manifest:
            raise AssertionError("repeated Copilot build changed manifest")
        print("PASS reproducible-copilot-adapter")

        config = MODULE.load_config()
        if manifest["core_version"] != config["core_version"]:
            raise AssertionError("manifest core version mismatch")
        if manifest["adapter_version"] != config["adapter_version"]:
            raise AssertionError("manifest adapter version mismatch")
        if manifest["compatibility_level"] != "Untested":
            raise AssertionError("unverified adapter must remain Untested")
        expected_commit, expected_dirty = MODULE.PACKAGE_HELPER.source_state()
        if manifest["source_commit"] != expected_commit or manifest["source_dirty"] is not expected_dirty:
            raise AssertionError("manifest source state does not match the current repository")
        if manifest["sha256"] != hashlib.sha256(archive.read_bytes()).hexdigest():
            raise AssertionError("manifest archive digest mismatch")
        if set(manifest["files"]) & set(manifest["excluded_core_files"]):
            raise AssertionError("excluded core file leaked into manifest file list")
        print("PASS copilot-manifest-contract")

        with zipfile.ZipFile(archive) as package:
            infos = package.infolist()
            names = [info.filename for info in infos]
            expected_names = [
                f"research-material-writer/{relative}" for relative in sorted(manifest["files"])
            ]
            if names != expected_names:
                raise AssertionError(f"unexpected Copilot archive file list: {names}")
            if any(info.date_time != MODULE.ZIP_TIMESTAMP for info in infos):
                raise AssertionError("Copilot archive contains variable timestamps")
            if any(info.create_system != 3 or info.external_attr >> 16 != MODULE.ZIP_FILE_MODE for info in infos):
                raise AssertionError("Copilot archive contains variable file metadata")
            skill_md = package.read("research-material-writer/SKILL.md").decode("utf-8")
            capability_map = package.read(
                "research-material-writer/references/copilot-readonly-capability-map.md"
            ).decode("utf-8")

        required_markers = (
            'argument-hint: "[research request or supplied sources]"',
            "disable-model-invocation: true",
            "user-invocable: true",
            "returns high-quality Chinese technical materials in chat",
            'repo_anatomy_core_version: "0.2.0-preview.1"',
            'repo_anatomy_adapter_version: "0.1.0"',
            "Do not execute shell or terminal commands",
            "Do not create, edit, delete, move, rename, or persist local files",
            "10. **Return and verify.**",
        )
        for marker in required_markers:
            if marker not in skill_md:
                raise AssertionError(f"generated Copilot SKILL.md missing marker: {marker}")

        forbidden_markers = (
            "allowed-tools:",
            "agent_created:",
            "references/quality-checklist.md",
            "scripts/check_draft.py",
            "workspace-file-maintainer",
            "**Persist and verify.**",
        )
        for marker in forbidden_markers:
            if marker in skill_md:
                raise AssertionError(f"generated Copilot SKILL.md leaked marker: {marker}")
        if "shell_execute" not in capability_map or "local_write" not in capability_map:
            raise AssertionError("capability map does not name prohibited portable capabilities")
        if skill_md.count("argument-hint:") != 1 or skill_md.count("user-invocable:") != 1 or skill_md.count("disable-model-invocation:") != 1:
            raise AssertionError("Copilot host extension fields must each appear exactly once")
        standard_projection = "\n".join(
            line
            for line in skill_md.splitlines()
            if not line.startswith(("argument-hint:", "user-invocable:", "disable-model-invocation:"))
        )
        if any(marker in standard_projection for marker in ("argument-hint:", "user-invocable:", "disable-model-invocation:")):
            raise AssertionError("standard projection retained Copilot host extension fields")
        print("PASS copilot-readonly-boundary")
        print("PASS copilot-standard-projection")

        manifest_path = archive.with_suffix(".manifest.json")
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        checksum_path = MODULE.PACKAGE_HELPER.write_checksum_file(output, [archive, manifest_path])
        lines = checksum_path.read_text(encoding="utf-8").splitlines()
        if len(lines) != 2:
            raise AssertionError("Copilot SHA256SUMS must contain exactly two entries")
        for line in lines:
            digest, name = line.split("  ", 1)
            path = output / name
            if digest != hashlib.sha256(path.read_bytes()).hexdigest():
                raise AssertionError(f"Copilot checksum mismatch for {name}")
        print("PASS copilot-checksums")

    print("Copilot adapter packaging tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
