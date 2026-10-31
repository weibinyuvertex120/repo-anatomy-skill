#!/usr/bin/env python3
"""Regression tests for versioned stable Skill installation."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PACKAGER = load_module("package_skills", ROOT / "scripts/package_skills.py")
INSTALLER = load_module("install_stable", ROOT / "scripts/install_stable.py")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="stable-install-tests-") as temporary:
        root = Path(temporary)
        packages = root / "packages"
        installs = root / "installs"
        archive, manifest = PACKAGER.package_skill("research-material-writer", packages, "workbuddy")
        manifest_path = archive.with_suffix(".manifest.json")
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        installed = INSTALLER.install(archive, manifest_path, installs, "workbuddy")
        if installed.is_symlink() or not (installed / "SKILL.md").is_file():
            raise AssertionError("stable installation was not copied correctly")
        receipt = json.loads((installed / ".install-receipt.json").read_text(encoding="utf-8"))
        if receipt["sha256"] != manifest["sha256"]:
            raise AssertionError("installation receipt does not match package")
        print("PASS installs-versioned-copy")

        try:
            INSTALLER.install(archive, manifest_path, installs, "workbuddy")
        except INSTALLER.InstallError as exc:
            if "already exists" not in str(exc):
                raise AssertionError(f"unexpected duplicate-install error: {exc}") from exc
            print("PASS rejects-existing-installation")
        else:
            raise AssertionError("duplicate stable installation must be rejected")

        bad_manifest = dict(manifest)
        bad_manifest["sha256"] = "0" * 64
        bad_manifest_path = packages / "bad.manifest.json"
        bad_manifest_path.write_text(json.dumps(bad_manifest), encoding="utf-8")
        try:
            INSTALLER.verify_archive(archive, bad_manifest_path, "workbuddy")
        except INSTALLER.InstallError as exc:
            if "SHA-256" not in str(exc):
                raise AssertionError(f"unexpected checksum error: {exc}") from exc
            print("PASS rejects-bad-checksum")
        else:
            raise AssertionError("bad checksum must be rejected")
    print("Stable installation regression tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
