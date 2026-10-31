#!/usr/bin/env python3
"""Create safe WorkBuddy and open-spec Skill ZIP packages."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("workspace-file-maintainer", "research-material-writer")
VARIANTS = ("workbuddy", "open-spec")
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
ZIP_FILE_MODE = 0o100644


class PackageError(Exception):
    pass


def collect_files(skill_root: Path) -> list[Path]:
    resolved_root = skill_root.resolve(strict=True)
    files: list[Path] = []
    for path in sorted(skill_root.rglob("*")):
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise PackageError(f"symlink is not allowed: {path.relative_to(skill_root)}")
        if stat.S_ISDIR(mode):
            continue
        if not stat.S_ISREG(mode):
            raise PackageError(f"non-regular file is not allowed: {path.relative_to(skill_root)}")
        resolved = path.resolve(strict=True)
        try:
            resolved.relative_to(resolved_root)
        except ValueError as exc:
            raise PackageError(f"path escapes Skill root: {path.relative_to(skill_root)}") from exc
        files.append(path)
    if not files:
        raise PackageError(f"Skill contains no files: {skill_root}")
    return files


def source_state() -> tuple[str, bool]:
    revision = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    status = subprocess.run(
        ["git", "-C", str(ROOT), "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=False,
    )
    commit = revision.stdout.strip() if revision.returncode == 0 else "unknown"
    dirty = status.returncode != 0 or bool(status.stdout.strip())
    return commit, dirty


def transform_skill_md(content: bytes, variant: str) -> bytes:
    if variant == "workbuddy":
        return content
    text = content.decode("utf-8")
    transformed, count = re.subn(r"^agent_created:\s*true\s*\n", "", text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise PackageError("open-spec package expected exactly one agent_created: true field")
    return transformed.encode("utf-8")


def package_skill(skill_name: str, output_dir: Path, variant: str = "workbuddy") -> tuple[Path, dict[str, object]]:
    if skill_name not in SKILLS:
        raise PackageError(f"unknown Skill: {skill_name}")
    if variant not in VARIANTS:
        raise PackageError(f"unknown package variant: {variant}")
    skill_root = ROOT / "skills" / skill_name
    if not skill_root.is_dir():
        raise PackageError(f"Skill directory does not exist: {skill_root}")

    files = collect_files(skill_root)
    skill_md = (skill_root / "SKILL.md").read_text(encoding="utf-8")
    version_match = re.search(r"""^\s+version:\s*["']([^"']+)["']\s*$""", skill_md, re.MULTILINE)
    if not version_match:
        raise PackageError(f"cannot read metadata.version: {skill_root / 'SKILL.md'}")
    version = version_match.group(1)

    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"{skill_name}-{variant}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as package:
        for path in files:
            relative = path.relative_to(skill_root).as_posix()
            content = path.read_bytes()
            if relative == "SKILL.md":
                content = transform_skill_md(content, variant)
            archive_path = f"{skill_name}/{relative}"
            info = zipfile.ZipInfo(archive_path, date_time=ZIP_TIMESTAMP)
            info.create_system = 3
            info.external_attr = ZIP_FILE_MODE << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            package.writestr(info, content)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    commit, dirty = source_state()
    manifest: dict[str, object] = {
        "skill": skill_name,
        "version": version,
        "variant": variant,
        "source_commit": commit,
        "source_dirty": dirty,
        "archive": archive.name,
        "sha256": digest,
        "files": [path.relative_to(skill_root).as_posix() for path in files],
    }
    return archive, manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path, help="directory for generated ZIP files")
    parser.add_argument("--variant", choices=(*VARIANTS, "all"), default="all")
    parser.add_argument("--require-clean", action="store_true", help="fail if the Git working tree is dirty")
    parser.add_argument("skills", nargs="*", choices=SKILLS)
    args = parser.parse_args()

    variants = VARIANTS if args.variant == "all" else (args.variant,)
    try:
        if args.require_clean and source_state()[1]:
            raise PackageError("release packaging requires a clean Git working tree")
        for skill_name in args.skills or SKILLS:
            for variant in variants:
                archive, manifest = package_skill(skill_name, args.output_dir.resolve(), variant)
                manifest_path = archive.with_suffix(".manifest.json")
                manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                print(f"Packaged {skill_name} ({variant}): {archive} (sha256={manifest['sha256']})")
    except (OSError, PackageError, zipfile.BadZipFile) as exc:
        print(f"Package failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
