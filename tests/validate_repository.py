#!/usr/bin/env python3
"""Validate the multi-skill source repository."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHANGELOG = ROOT / "CHANGELOG.md"
LICENSE = ROOT / "LICENSE"
RELEASE_WORKFLOW = ROOT / ".github/workflows/release.yml"
TAG_WORKFLOW = ROOT / ".github/workflows/verify-tags.yml"
FAILURE_WORKFLOW = ROOT / ".github/workflows/failure-notification.yml"


@dataclass(frozen=True)
class SkillConfig:
    name: str
    tools: frozenset[str]
    references: frozenset[str]
    scripts: frozenset[str]
    trigger_file: str
    functional_file: str
    minimum_groups: dict[str, int]

    @property
    def directory(self) -> Path:
        return ROOT / "skills" / self.name


SKILLS = (
    SkillConfig(
        name="workspace-file-maintainer",
        tools=frozenset({"Read", "Write", "Edit", "Glob", "Grep", "Bash"}),
        references=frozenset(
            {
                "references/workflow.md",
                "references/safety-boundaries.md",
                "references/error-handling.md",
                "references/evaluation-cases.md",
            }
        ),
        scripts=frozenset(),
        trigger_file="evals/trigger-cases.json",
        functional_file="evals/functional-cases.md",
        minimum_groups={"must_trigger": 4, "paraphrase": 3, "must_not_trigger": 4, "boundary": 2},
    ),
    SkillConfig(
        name="research-material-writer",
        tools=frozenset({"Read", "Write", "Edit", "Glob", "Grep", "Bash", "WebSearch", "WebFetch"}),
        references=frozenset(
            {
                "references/source-and-verification.md",
                "references/research-workflow.md",
                "references/tutorial-writing.md",
                "references/project-analysis.md",
                "references/comparison-writing.md",
                "references/open-source-onboarding.md",
                "references/quality-checklist.md",
            }
        ),
        scripts=frozenset({"scripts/check_draft.py"}),
        trigger_file="evals/research-trigger-cases.json",
        functional_file="evals/research-functional-cases.md",
        minimum_groups={"must_trigger": 4, "paraphrase": 3, "must_not_trigger": 5, "boundary": 2},
    ),
)

REQUIRED_SHARED_FILES = {
    "evals/acceptance-results.md",
    "evals/real-project-markitdown-2026-10-30.md",
    "evals/real-project-markitdown-onboarding-2026-10-31.md",
    "tests/test_validator.py",
    "tests/test_draft_checker.py",
    "tests/validate_copilot_evals.py",
    "tests/test_copilot_evals.py",
    "evals/copilot-readonly-cases.json",
    "evals/copilot-readonly-evidence-contract.json",
    "evals/copilot-readonly-run.schema.json",
    "evals/copilot-readonly-manual/README.md",
    "evals/copilot-readonly-manual/operator-checklist.md",
    "evals/copilot-readonly-manual/prompts.md",
    "evals/copilot-readonly-manual/environment-record.json",
    "evals/copilot-readonly-manual/run-record.template.json",
    "evals/copilot-readonly-manual/evidence-index.template.md",
    "adapters/github-copilot/research-material-writer/adapter.json",
    "adapters/github-copilot/research-material-writer/SKILL.overlay.md",
    "adapters/github-copilot/research-material-writer/references/copilot-readonly-capability-map.md",
    "scripts/package_copilot_adapter.py",
    "tests/test_copilot_adapter.py",
}

REQUIRED_WFM_FIXTURES = {
    "evals/fixtures/create-file/request.md",
    "evals/fixtures/modify-existing/guide.md",
    "evals/fixtures/modify-existing/request.md",
    "evals/fixtures/ambiguous-match/status.md",
    "evals/fixtures/outside-workspace/case.md",
    "evals/fixtures/sensitive-file/.env.fixture",
    "evals/fixtures/sensitive-file/case.md",
    "evals/fixtures/binary-file/sample.bin",
    "evals/fixtures/binary-file/case.md",
    "evals/fixtures/continuous-iteration/draft.md",
    "evals/fixtures/continuous-iteration/session-a-request.md",
    "evals/fixtures/continuous-iteration/session-b-request.md",
}

PLACEHOLDER_PATTERNS = (
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
    re.compile(r"\[insert .+?\]", re.IGNORECASE),
    re.compile(r"example_(?:script|reference|asset)", re.IGNORECASE),
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def parse_frontmatter(text: str, errors: list[str], skill_name: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(errors, f"{skill_name}: SKILL.md has invalid or missing YAML frontmatter")
        return {}

    result: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        if not raw_line.strip() or raw_line.startswith("  "):
            continue
        if ":" not in raw_line:
            fail(errors, f"{skill_name}: unsupported frontmatter line: {raw_line}")
            continue
        key, value = raw_line.split(":", 1)
        result[key.strip()] = value.strip().strip('"')
    return result


def validate_skill(config: SkillConfig, errors: list[str]) -> str:
    skill_md = config.directory / "SKILL.md"
    if not skill_md.is_file():
        fail(errors, f"Missing {skill_md.relative_to(ROOT)}")
        return ""

    text = skill_md.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text, errors, config.name)
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")

    if name != config.name:
        fail(errors, f"{config.name}: frontmatter name is '{name}'")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        fail(errors, f"{config.name}: name is not valid kebab-case")
    if "This skill should be used when" not in description:
        fail(errors, f"{config.name}: description must state when the skill should be used")
    if len(description) < 120 or len(description) > 1024:
        fail(errors, f"{config.name}: description length must be 120-1024 characters, got {len(description)}")
    if frontmatter.get("license") != "MIT":
        fail(errors, f"{config.name}: frontmatter license must be MIT")
    if frontmatter.get("agent_created") != "true":
        fail(errors, f"{config.name}: frontmatter must include agent_created: true")

    allowed = frozenset(frontmatter.get("allowed-tools", "").split())
    if allowed != config.tools:
        fail(errors, f"{config.name}: allowed-tools mismatch: {sorted(allowed)}")

    if len(text.splitlines()) >= 500:
        fail(errors, f"{config.name}: SKILL.md must remain below 500 lines")

    body = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern.search(body):
            fail(errors, f"{config.name}: SKILL.md contains placeholder pattern: {pattern.pattern}")

    referenced = frozenset(re.findall(r"\((references/[^)]+\.md)\)", text))
    if referenced != config.references:
        fail(errors, f"{config.name}: referenced files mismatch: {sorted(referenced)}")

    for relative in config.references | config.scripts:
        resource = config.directory / relative
        if resource.is_symlink():
            fail(errors, f"{config.name}: symlink is not allowed: {relative}")
        if not resource.is_file():
            fail(errors, f"Missing skill resource: {config.name}/{relative}")

    intended_files = frozenset({"SKILL.md"}) | config.references | config.scripts
    actual_files_set: set[str] = set()
    for path in config.directory.rglob("*"):
        if path.is_symlink():
            fail(errors, f"{config.name}: symlink is not allowed: {path.relative_to(config.directory).as_posix()}")
            continue
        if path.is_file():
            actual_files_set.add(path.relative_to(config.directory).as_posix())
    actual_files = frozenset(actual_files_set)
    if actual_files != intended_files:
        fail(errors, f"{config.name}: unexpected package files: {sorted(actual_files - intended_files)}")

    version_match = re.search(r'^\s+version:\s*["\']([^"\']+)["\']\s*$', text, re.MULTILINE)
    version = version_match.group(1) if version_match else ""
    semver = re.compile(
        r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"
        r"(?:-(?:0|[1-9]\d*|[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9]\d*|[A-Za-z-][0-9A-Za-z-]*))*)?"
    )
    if not semver.fullmatch(version):
        fail(errors, f"{config.name}: invalid metadata.version '{version}'")
    return version


def validate_evaluations(config: SkillConfig, version: str, errors: list[str]) -> None:
    trigger_path = ROOT / config.trigger_file
    functional_path = ROOT / config.functional_file
    if not trigger_path.is_file():
        fail(errors, f"Missing {config.trigger_file}")
        return
    if not functional_path.is_file():
        fail(errors, f"Missing {config.functional_file}")
    elif config.name == "research-material-writer":
        functional_text = functional_path.read_text(encoding="utf-8")
        required_sections = (
            "# Research Material Writer Functional Evaluation",
            "## R01 - Beginner Tutorial From Primary Sources",
            "## R02 - Open-Source Project Onboarding",
            "## R08 - Negative Simple File Task",
            "## Release Record",
        )
        for heading in required_sections:
            if heading not in functional_text:
                fail(errors, f"{config.functional_file}: missing required section {heading}")
        if len(re.findall(r"^## R\d{2} - ", functional_text, re.MULTILINE)) < 8:
            fail(errors, f"{config.functional_file}: expected at least 8 functional cases")

    try:
        data = json.loads(trigger_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(errors, f"{config.trigger_file} is invalid JSON: {exc}")
        return

    if data.get("skill") != config.name:
        fail(errors, f"{config.trigger_file}: skill does not match {config.name}")
    if version and data.get("version") != version:
        fail(errors, f"{config.trigger_file}: version does not match {version}")

    cases = data.get("cases")
    if not isinstance(cases, list) or len(cases) < 12:
        fail(errors, f"{config.trigger_file}: must contain at least 12 cases")
        return

    ids: set[str] = set()
    prompts: dict[str, str] = {}
    groups: dict[str, int] = {}
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            fail(errors, f"{config.trigger_file}: case {index} is not an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            fail(errors, f"{config.trigger_file}: case {index} has no id")
        elif case_id in ids:
            fail(errors, f"{config.trigger_file}: duplicate id {case_id}")
        else:
            ids.add(case_id)
        for required in ("group", "prompt", "expected_skill", "expected_behavior"):
            if required not in case:
                fail(errors, f"{config.trigger_file}: case {case_id or index} missing {required}")
        for field in ("group", "prompt", "expected_behavior"):
            value = case.get(field)
            if not isinstance(value, str) or not value.strip():
                fail(errors, f"{config.trigger_file}: case {case_id or index} {field} must be a non-empty string")
        if not isinstance(case.get("expected_skill"), bool):
            fail(errors, f"{config.trigger_file}: case {case_id or index} expected_skill must be a boolean")
        group = case.get("group")
        if isinstance(group, str):
            if group not in config.minimum_groups:
                fail(errors, f"{config.trigger_file}: case {case_id or index} has unknown group '{group}'")
            groups[group] = groups.get(group, 0) + 1
        prompt = case.get("prompt")
        if isinstance(prompt, str) and prompt.strip():
            normalized_prompt = re.sub(r"\s+", " ", prompt).strip().casefold()
            if normalized_prompt in prompts:
                fail(errors, f"{config.trigger_file}: duplicate prompt in cases {prompts[normalized_prompt]} and {case_id or index}")
            else:
                prompts[normalized_prompt] = case_id or str(index)

    for group, minimum in config.minimum_groups.items():
        if groups.get(group, 0) < minimum:
            fail(errors, f"{config.trigger_file}: group '{group}' needs at least {minimum} cases")


def validate_copilot_evaluations(errors: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "tests/validate_copilot_evals.py")],
        cwd=ROOT,
        env={"PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        output = (result.stdout + result.stderr).strip()
        fail(errors, f"Copilot evaluation contract validation failed: {output}")


def validate_copilot_adapter(errors: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "tests/test_copilot_adapter.py")],
        cwd=ROOT,
        env={"PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        output = (result.stdout + result.stderr).strip()
        fail(errors, f"Copilot adapter validation failed: {output}")


def validate_license(errors: list[str]) -> None:
    if not LICENSE.is_file():
        fail(errors, "Missing LICENSE")
        return
    text = LICENSE.read_text(encoding="utf-8")
    if not text.startswith("MIT License\n") or "Copyright (c) 2026 Veretex" not in text:
        fail(errors, "LICENSE is not the expected MIT license for Veretex")


def validate_changelog(versions: dict[str, str], errors: list[str]) -> None:
    if not CHANGELOG.is_file():
        fail(errors, "Missing CHANGELOG.md")
        return
    text = CHANGELOG.read_text(encoding="utf-8")
    for skill_name, version in versions.items():
        marker = f"## {skill_name} {version}"
        legacy_marker = f"## {version}"
        if marker not in text and not (skill_name == "workspace-file-maintainer" and legacy_marker in text):
            fail(errors, f"CHANGELOG.md has no entry for {skill_name} {version}")


def validate_acceptance_manifest(errors: list[str]) -> None:
    path = ROOT / "evals/acceptance-results.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    required = (
        "## Verification Record",
        "- skill_versions:",
        "- host:",
        "- evidence_scope:",
        "- source_revision:",
        "- package_scope:",
        "- routing_scope:",
    )
    for marker in required:
        if marker not in text:
            fail(errors, f"evals/acceptance-results.md: missing manifest field {marker}")


def validate_shared_files(errors: list[str]) -> None:
    for relative in REQUIRED_SHARED_FILES | REQUIRED_WFM_FIXTURES:
        if not (ROOT / relative).is_file():
            fail(errors, f"Missing repository file: {relative}")


def validate_release_workflows(errors: list[str]) -> None:
    for path in (RELEASE_WORKFLOW, TAG_WORKFLOW, FAILURE_WORKFLOW):
        if not path.is_file():
            fail(errors, f"Missing {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped.startswith("uses:"):
                continue
            value = stripped.split(":", 1)[1].strip()
            if value.startswith("./"):
                continue
            if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}(?:\s+#.*)?", value):
                fail(errors, f"{path.relative_to(ROOT)}: action is not pinned to a full commit SHA: {value}")

    if RELEASE_WORKFLOW.is_file():
        release_text = RELEASE_WORKFLOW.read_text(encoding="utf-8")
        required = (
            "workflow_dispatch:",
            "release_sha:",
            "tag:",
            "environment: release",
            "permissions:\n      contents: write",
            "sha256sum -c SHA256SUMS --strict",
            "git verify-tag",
            "gpg.ssh.allowedSignersFile",
            "GitHub release asset digests verified",
            'test "$(git rev-parse HEAD)" = "$RELEASE_SHA"',
        )
        for marker in required:
            if marker not in release_text:
                fail(errors, f".github/workflows/release.yml: missing release gate {marker}")

    if TAG_WORKFLOW.is_file():
        tag_text = TAG_WORKFLOW.read_text(encoding="utf-8")
        for marker in ('tags:\n      - "v*"', "git verify-tag", 'test "$(git cat-file -t "$RELEASE_TAG")" = "tag"'):
            if marker not in tag_text:
                fail(errors, f".github/workflows/verify-tags.yml: missing tag gate {marker}")

    if FAILURE_WORKFLOW.is_file():
        failure_text = FAILURE_WORKFLOW.read_text(encoding="utf-8")
        required = ("workflow_run:", "issues: write", "github.event.workflow_run.conclusion == 'failure'", "gh issue create")
        for marker in required:
            if marker not in failure_text:
                fail(errors, f".github/workflows/failure-notification.yml: missing notification gate {marker}")


def validate_repository_hygiene(errors: list[str]) -> None:
    forbidden_names = {".DS_Store", "__pycache__"}
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or "dist" in path.parts:
            continue
        if path.name not in forbidden_names and path.suffix != ".pyc":
            continue
        relative = path.relative_to(ROOT).as_posix()
        ignored = subprocess.run(
            ["git", "-C", str(ROOT), "check-ignore", "-q", relative],
            check=False,
        ).returncode == 0
        if not ignored:
            fail(errors, f"Generated file is not ignored: {relative}")


def main() -> int:
    errors: list[str] = []
    versions: dict[str, str] = {}
    for config in SKILLS:
        versions[config.name] = validate_skill(config, errors)
        validate_evaluations(config, versions[config.name], errors)
    validate_copilot_evaluations(errors)
    validate_copilot_adapter(errors)
    validate_license(errors)
    validate_changelog(versions, errors)
    validate_shared_files(errors)
    validate_acceptance_manifest(errors)
    validate_release_workflows(errors)
    validate_repository_hygiene(errors)

    if errors:
        print(f"Repository validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Repository validation passed")
    for config in SKILLS:
        data = json.loads((ROOT / config.trigger_file).read_text(encoding="utf-8"))
        print(f"- {config.name}: version {versions[config.name]}, {len(data['cases'])} trigger cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
