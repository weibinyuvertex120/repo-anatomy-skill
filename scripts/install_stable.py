#!/usr/bin/env python3
"""Install a verified Skill archive without following development symlinks."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


class InstallError(Exception):
    pass


def verify_archive(archive: Path, manifest_path: Path, expected_variant: str) -> dict[str, object]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if manifest.get("sha256") != digest:
        raise InstallError("archive SHA-256 does not match manifest")
    if manifest.get("variant") != expected_variant:
        raise InstallError(f"expected {expected_variant} variant, got {manifest.get('variant')}")
    expected_files = manifest.get("files")
    if not isinstance(expected_files, list) or not expected_files:
        raise InstallError("manifest file list is missing or empty")
    skill = manifest.get("skill")
    if not isinstance(skill, str) or not skill:
        raise InstallError("manifest Skill name is missing")
    with zipfile.ZipFile(archive) as package:
        names = package.namelist()
        expected_names = [f"{skill}/{relative}" for relative in expected_files]
        if names != expected_names:
            raise InstallError("archive file list does not match manifest")
        for name in names:
            path = Path(name)
            if path.is_absolute() or ".." in path.parts:
                raise InstallError(f"unsafe archive path: {name}")
    return manifest


def install(archive: Path, manifest_path: Path, target_root: Path, variant: str) -> Path:
    manifest = verify_archive(archive, manifest_path, variant)
    skill = str(manifest["skill"])
    version = str(manifest["version"])
    install_root = target_root / f"{skill}-{version}-{variant}"
    if install_root.is_symlink():
        raise InstallError(f"refusing to replace symlink: {install_root}")
    if install_root.exists():
        raise InstallError(f"installation already exists: {install_root}")

    target_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="skill-install-", dir=target_root) as temporary:
        staging = Path(temporary)
        with zipfile.ZipFile(archive) as package:
            package.extractall(staging)
        source = staging / skill
        if not source.is_dir():
            raise InstallError(f"archive does not contain expected Skill directory: {skill}")
        shutil.copytree(source, install_root)
    receipt = install_root / ".install-receipt.json"
    receipt.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return install_root


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("target_root", type=Path)
    parser.add_argument("--variant", choices=("workbuddy", "open-spec"), required=True)
    args = parser.parse_args()

    try:
        installed = install(args.archive.resolve(), args.manifest.resolve(), args.target_root.resolve(), args.variant)
    except (OSError, json.JSONDecodeError, zipfile.BadZipFile, InstallError) as exc:
        print(f"Install failed: {exc}", file=sys.stderr)
        return 1
    print(f"Installed verified Skill: {installed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
