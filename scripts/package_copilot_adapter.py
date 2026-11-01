#!/usr/bin/env python3
"""Build the deterministic GitHub Copilot read-only adapter package."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CORE_ROOT = ROOT / "skills/research-material-writer"
ADAPTER_ROOT = ROOT / "adapters/github-copilot/research-material-writer"
CONFIG_PATH = ADAPTER_ROOT / "adapter.json"
PACKAGE_SCRIPT = ROOT / "scripts/package_skills.py"

SPEC = importlib.util.spec_from_file_location("package_skills", PACKAGE_SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load package helper: {PACKAGE_SCRIPT}")
PACKAGE_HELPER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PACKAGE_HELPER)

ZIP_TIMESTAMP = PACKAGE_HELPER.ZIP_TIMESTAMP
ZIP_FILE_MODE = PACKAGE_HELPER.ZIP_FILE_MODE
PackageError = PACKAGE_HELPER.PackageError


def load_config() -> dict[str, Any]:
    try:
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PackageError(f"cannot read adapter configuration: {exc}") from exc

    required = {
        "schema_version",
        "adapter",
        "adapter_version",
        "core_skill",
        "core_version",
        "target",
        "package",
        "frontmatter",
        "prohibited_capabilities",
    }
    missing = required - set(config)
    if missing:
        raise PackageError(f"adapter configuration missing fields: {sorted(missing)}")
    if config["core_skill"] != CORE_ROOT.name:
        raise PackageError(f"adapter core_skill must be {CORE_ROOT.name}")
    if config["package"]["skill_directory"] != CORE_ROOT.name:
        raise PackageError(f"adapter package directory must be {CORE_ROOT.name}")
    if config["frontmatter"] != {"user-invocable": True, "disable-model-invocation": True}:
        raise PackageError("adapter must remain explicitly invocable and model invocation must be disabled")
    return config


def parse_core_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not match:
        raise PackageError("core SKILL.md has invalid frontmatter")

    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if line.startswith("  ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"')

    version_match = re.search(r'^\s+version:\s*["\']([^"\']+)["\']\s*$', match.group(1), re.MULTILINE)
    if version_match:
        values["metadata.version"] = version_match.group(1)
    return values, match.group(2)


def build_frontmatter(config: dict[str, Any], core_values: dict[str, str]) -> str:
    core_version = config["core_version"]
    if core_values.get("metadata.version") != core_version:
        raise PackageError(
            f"adapter core_version {core_version} does not match source Skill {core_values.get('metadata.version')!r}"
        )
    if core_values.get("name") != config["core_skill"]:
        raise PackageError("adapter core Skill name does not match source Skill")
    if core_values.get("license") != "MIT":
        raise PackageError("adapter expects the core Skill to use the MIT license")

    description = core_values.get("description", "")
    if not description:
        raise PackageError("core Skill description is missing")
    description_prefix = "Researches, verifies, structures, and writes high-quality Chinese technical materials"
    adapted_prefix = "Researches, verifies, structures, and returns high-quality Chinese technical materials in chat"
    if description.count(description_prefix) != 1:
        raise PackageError("core Skill description changed; review the Copilot read-only description transformation")
    description = description.replace(description_prefix, adapted_prefix, 1)
    compatibility = (
        "GitHub Copilot in Visual Studio Code Agent Mode. Explicit invocation only. "
        "Requires read-only public-source or user-provided material access. "
        "Local file writes, edits, and shell execution are prohibited."
    )
    return "\n".join(
        (
            "---",
            f"name: {config['core_skill']}",
            f"description: {description}",
            "license: MIT",
            f"compatibility: {compatibility}",
            'argument-hint: "[research request or supplied sources]"',
            "user-invocable: true",
            "disable-model-invocation: true",
            "metadata:",
            f'  version: "{core_version}"',
            f'  repo_anatomy_core_version: "{core_version}"',
            f'  repo_anatomy_adapter_version: "{config["adapter_version"]}"',
            f'  repo_anatomy_adapter: "{config["adapter"]}"',
            '  category: "writing"',
            '  scope: "researched-technical-materials-readonly"',
            "---",
            "",
        )
    )


def build_skill_md(config: dict[str, Any]) -> bytes:
    core_text = (CORE_ROOT / "SKILL.md").read_text(encoding="utf-8")
    core_values, body = parse_core_frontmatter(core_text)
    quality_marker = "\n## Quality Gate\n"
    if body.count(quality_marker) != 1:
        raise PackageError("core SKILL.md must contain exactly one Quality Gate section")
    body = body.split(quality_marker, 1)[0].rstrip() + "\n"

    old_step = (
        "10. **Persist and verify.** Write the requested file conservatively, re-read it, "
        "run the bundled draft checker when applicable, and report remaining risks."
    )
    new_step = (
        "10. **Return and verify.** Check the complete chat response against the collected evidence, "
        "disclose remaining risks, and report that no local file or shell action was performed."
    )
    if body.count(old_step) != 1:
        raise PackageError("core SKILL.md persistence step changed; review the adapter transformation")
    body = body.replace(old_step, new_step, 1)

    intro = (
        "# Research Material Writer\n\n"
        "Produce Chinese technical materials through evidence-led research and task-oriented writing. "
        "Treat source collection, factual verification, document design, drafting, and file persistence as separate stages.\n"
    )
    adapted_intro = (
        "# Research Material Writer\n\n"
        "Produce Chinese technical materials through evidence-led research and task-oriented writing. "
        "Treat source collection, factual verification, document design, drafting, and chat-response delivery as separate stages.\n"
    )
    if body.count(intro) != 1:
        raise PackageError("core SKILL.md introduction changed; review the adapter insertion point")
    body = body.replace(intro, adapted_intro, 1)

    persistence_boundary = (
        "- Do not use this skill as a substitute for ordinary file editing. Delegate final persistence to "
        "`workspace-file-maintainer` or apply its inspect-edit-re-read discipline."
    )
    adapted_boundary = (
        "- Do not use this Skill as a substitute for file maintenance. Return the complete result in chat; "
        "file persistence requires a separately approved workflow outside this read-only adapter."
    )
    if body.count(persistence_boundary) != 1:
        raise PackageError("core SKILL.md persistence boundary changed; review the adapter transformation")
    body = body.replace(persistence_boundary, adapted_boundary, 1)

    overlay = (ADAPTER_ROOT / "SKILL.overlay.md").read_text(encoding="utf-8").strip()
    body = body.replace(adapted_intro, f"{adapted_intro}\n{overlay}\n", 1)

    generated = build_frontmatter(config, core_values) + body
    forbidden = (
        "allowed-tools:",
        "agent_created:",
        "references/quality-checklist.md",
        "scripts/check_draft.py",
        "**Persist and verify.**",
        "file persistence as separate stages",
        "Delegate final persistence",
        "workspace-file-maintainer",
    )
    for marker in forbidden:
        if marker in generated:
            raise PackageError(f"generated Copilot SKILL.md contains prohibited marker: {marker}")
    return generated.encode("utf-8")


def collect_package_files(config: dict[str, Any]) -> dict[str, bytes]:
    package = config["package"]
    core_files = package["core_files"]
    adapter_files = package["adapter_files"]
    excluded_files = package["excluded_core_files"]
    if len(core_files) != len(set(core_files)) or len(adapter_files) != len(set(adapter_files)):
        raise PackageError("adapter file lists contain duplicates")
    if set(core_files) & set(excluded_files):
        raise PackageError("adapter core_files and excluded_core_files overlap")

    actual_core_files = {
        path.relative_to(CORE_ROOT).as_posix() for path in PACKAGE_HELPER.collect_files(CORE_ROOT)
    }
    classified_core_files = set(core_files) | set(excluded_files)
    if actual_core_files != classified_core_files:
        raise PackageError(
            "adapter must classify every core file explicitly: "
            f"unclassified={sorted(actual_core_files - classified_core_files)}, "
            f"missing={sorted(classified_core_files - actual_core_files)}"
        )

    expected_adapter_sources = {
        "adapter.json",
        "SKILL.overlay.md",
        *adapter_files,
    }
    actual_adapter_sources = {
        path.relative_to(ADAPTER_ROOT).as_posix() for path in PACKAGE_HELPER.collect_files(ADAPTER_ROOT)
    }
    if actual_adapter_sources != expected_adapter_sources:
        raise PackageError(
            "adapter source files do not match the declared source layout: "
            f"unexpected={sorted(actual_adapter_sources - expected_adapter_sources)}, "
            f"missing={sorted(expected_adapter_sources - actual_adapter_sources)}"
        )

    selected: dict[str, bytes] = {}
    for relative in core_files:
        path = CORE_ROOT / relative
        if relative == "SKILL.md":
            selected[relative] = build_skill_md(config)
            continue
        if path.is_symlink() or not path.is_file():
            raise PackageError(f"invalid core adapter file: {relative}")
        selected[relative] = path.read_bytes()

    for relative in excluded_files:
        path = CORE_ROOT / relative
        if path.is_symlink() or not path.is_file():
            raise PackageError(f"invalid excluded core file: {relative}")

    for relative in adapter_files:
        path = ADAPTER_ROOT / relative
        if path.is_symlink() or not path.is_file():
            raise PackageError(f"invalid adapter file: {relative}")
        if relative in selected:
            raise PackageError(f"adapter file collides with selected core file: {relative}")
        selected[relative] = path.read_bytes()

    referenced = set(re.findall(rb"\((references/[^)]+\.md)\)", selected["SKILL.md"]))
    decoded_references = {item.decode("utf-8") for item in referenced}
    packaged_references = {name for name in selected if name.startswith("references/")}
    if decoded_references != packaged_references:
        raise PackageError(
            f"generated SKILL.md references do not match packaged references: "
            f"referenced={sorted(decoded_references)}, packaged={sorted(packaged_references)}"
        )
    return selected


def package_adapter(output_dir: Path) -> tuple[Path, dict[str, Any]]:
    config = load_config()
    files = collect_package_files(config)
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_name = f"{config['core_skill']}-{config['adapter']}.zip"
    archive = output_dir / archive_name
    skill_directory = config["package"]["skill_directory"]

    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as package:
        for relative, content in sorted(files.items()):
            archive_path = f"{skill_directory}/{relative}"
            info = zipfile.ZipInfo(archive_path, date_time=ZIP_TIMESTAMP)
            info.create_system = 3
            info.external_attr = ZIP_FILE_MODE << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            package.writestr(info, content)

    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    commit, dirty = PACKAGE_HELPER.source_state()
    manifest: dict[str, Any] = {
        "skill": config["core_skill"],
        "core_version": config["core_version"],
        "adapter": config["adapter"],
        "adapter_version": config["adapter_version"],
        "variant": "github-copilot-vscode-readonly",
        "compatibility_level": "Untested",
        "target": config["target"],
        "source_commit": commit,
        "source_dirty": dirty,
        "archive": archive.name,
        "sha256": digest,
        "files": sorted(files),
        "core_files": config["package"]["core_files"],
        "adapter_files": config["package"]["adapter_files"],
        "excluded_core_files": config["package"]["excluded_core_files"],
        "prohibited_capabilities": config["prohibited_capabilities"],
    }
    return archive, manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path, help="directory for the Copilot adapter ZIP and manifest")
    parser.add_argument("--require-clean", action="store_true", help="fail if the Git working tree is dirty")
    args = parser.parse_args()

    try:
        if args.require_clean and PACKAGE_HELPER.source_state()[1]:
            raise PackageError("adapter packaging requires a clean Git working tree")
        output_dir = args.output_dir.resolve()
        archive, manifest = package_adapter(output_dir)
        manifest_path = archive.with_suffix(".manifest.json")
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        checksum_path = PACKAGE_HELPER.write_checksum_file(output_dir, [archive, manifest_path])
        print(f"Packaged {manifest['adapter']}: {archive} (sha256={manifest['sha256']})")
        print(f"Wrote manifest: {manifest_path}")
        print(f"Wrote checksums: {checksum_path}")
    except (OSError, PackageError, zipfile.BadZipFile) as exc:
        print(f"Copilot adapter packaging failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
