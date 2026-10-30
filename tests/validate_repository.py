#!/usr/bin/env python3
"""Validate the workspace-file-maintainer source repository."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "workspace-file-maintainer"
SKILL_MD = SKILL_DIR / "SKILL.md"
CHANGELOG = ROOT / "CHANGELOG.md"
TRIGGER_CASES = ROOT / "evals" / "trigger-cases.json"
FUNCTIONAL_CASES = ROOT / "evals" / "functional-cases.md"
ACCEPTANCE_RESULTS = ROOT / "evals" / "acceptance-results.md"

REQUIRED_REFERENCES = {
    "references/workflow.md",
    "references/safety-boundaries.md",
    "references/error-handling.md",
    "references/evaluation-cases.md",
}

REQUIRED_FIXTURES = {
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


def parse_frontmatter(text: str, errors: list[str]) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(errors, "SKILL.md has invalid or missing YAML frontmatter")
        return {}

    result: dict[str, str] = {}
    current_key: str | None = None
    for raw_line in match.group(1).splitlines():
        if not raw_line.strip() or raw_line.startswith("  "):
            continue
        if ":" not in raw_line:
            fail(errors, f"Unsupported frontmatter line: {raw_line}")
            continue
        key, value = raw_line.split(":", 1)
        current_key = key.strip()
        result[current_key] = value.strip().strip('"')

    if current_key is None:
        fail(errors, "SKILL.md frontmatter is empty")
    return result


def validate_skill(errors: list[str]) -> tuple[str, str]:
    if not SKILL_MD.is_file():
        fail(errors, f"Missing {SKILL_MD.relative_to(ROOT)}")
        return "", ""

    text = SKILL_MD.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text, errors)
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")

    if name != SKILL_DIR.name:
        fail(errors, f"Skill name '{name}' does not match directory '{SKILL_DIR.name}'")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        fail(errors, f"Skill name '{name}' is not valid kebab-case")
    if not description:
        fail(errors, "Frontmatter description is missing")
    if "This skill should be used when" not in description:
        fail(errors, "Description must state when the skill should be used")
    if len(description) < 120 or len(description) > 1024:
        fail(errors, f"Description length must be 120-1024 characters, got {len(description)}")
    if frontmatter.get("agent_created") != "true":
        fail(errors, "Frontmatter must include agent_created: true")

    allowed = set(frontmatter.get("allowed-tools", "").split())
    expected_tools = {"Read", "Write", "Edit", "Glob", "Grep", "Bash"}
    if allowed != expected_tools:
        fail(errors, f"allowed-tools must be exactly {sorted(expected_tools)}, got {sorted(allowed)}")

    line_count = len(text.splitlines())
    if line_count >= 500:
        fail(errors, f"SKILL.md must remain below 500 lines, got {line_count}")

    body_without_frontmatter = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern.search(body_without_frontmatter):
            fail(errors, f"SKILL.md contains placeholder pattern: {pattern.pattern}")

    referenced = set(re.findall(r"\((references/[^)]+\.md)\)", text))
    missing_links = REQUIRED_REFERENCES - referenced
    if missing_links:
        fail(errors, f"SKILL.md does not link required references: {sorted(missing_links)}")
    extra_links = referenced - REQUIRED_REFERENCES
    if extra_links:
        fail(errors, f"SKILL.md links undeclared references: {sorted(extra_links)}")

    for relative in REQUIRED_REFERENCES:
        path = SKILL_DIR / relative
        if not path.is_file():
            fail(errors, f"Missing skill reference: {path.relative_to(ROOT)}")

    for forbidden in (SKILL_DIR / "scripts", SKILL_DIR / "assets", SKILL_DIR / "README.md"):
        if forbidden.exists():
            fail(errors, f"First release must not contain {forbidden.relative_to(ROOT)}")

    skill_files = {path.relative_to(SKILL_DIR).as_posix() for path in SKILL_DIR.rglob("*") if path.is_file()}
    intended_files = {"SKILL.md", *REQUIRED_REFERENCES}
    if skill_files != intended_files:
        fail(errors, f"Unexpected skill package files: {sorted(skill_files - intended_files)}")

    version_match = re.search(r'^\s+version:\s*["\']([^"\']+)["\']\s*$', text, re.MULTILINE)
    version = version_match.group(1) if version_match else ""
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail(errors, f"metadata.version is missing or invalid: '{version}'")

    return text, version


def validate_changelog(errors: list[str], version: str) -> None:
    if not CHANGELOG.is_file():
        fail(errors, "Missing CHANGELOG.md")
        return
    text = CHANGELOG.read_text(encoding="utf-8")
    if version and not re.search(rf"^## {re.escape(version)}(?:\s|$)", text, re.MULTILINE):
        fail(errors, f"CHANGELOG.md has no heading for version {version}")


def validate_evaluations(errors: list[str], version: str) -> None:
    if not TRIGGER_CASES.is_file():
        fail(errors, "Missing evals/trigger-cases.json")
        return
    if not FUNCTIONAL_CASES.is_file():
        fail(errors, "Missing evals/functional-cases.md")
    if not ACCEPTANCE_RESULTS.is_file():
        fail(errors, "Missing evals/acceptance-results.md")

    try:
        data = json.loads(TRIGGER_CASES.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(errors, f"trigger-cases.json is invalid JSON: {exc}")
        return

    if data.get("skill") != SKILL_DIR.name:
        fail(errors, "trigger-cases.json skill does not match the skill directory")
    if version and data.get("version") != version:
        fail(errors, f"trigger-cases.json version does not match {version}")

    cases = data.get("cases")
    if not isinstance(cases, list) or len(cases) < 12:
        fail(errors, "trigger-cases.json must contain at least 12 cases")
        return

    ids: set[str] = set()
    groups: dict[str, int] = {}
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            fail(errors, f"Trigger case {index} is not an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            fail(errors, f"Trigger case {index} has no id")
        elif case_id in ids:
            fail(errors, f"Duplicate trigger case id: {case_id}")
        else:
            ids.add(case_id)
        for required in ("group", "prompt", "expected_skill", "expected_behavior"):
            if required not in case:
                fail(errors, f"Trigger case {case_id or index} is missing {required}")
        group = case.get("group")
        if isinstance(group, str):
            groups[group] = groups.get(group, 0) + 1

    minimums = {"must_trigger": 4, "paraphrase": 3, "must_not_trigger": 4, "boundary": 2}
    for group, minimum in minimums.items():
        if groups.get(group, 0) < minimum:
            fail(errors, f"Trigger group '{group}' needs at least {minimum} cases")

    for relative in REQUIRED_FIXTURES:
        if not (ROOT / relative).is_file():
            fail(errors, f"Missing fixture file: {relative}")


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
    _, version = validate_skill(errors)
    validate_changelog(errors, version)
    validate_evaluations(errors, version)
    validate_repository_hygiene(errors)

    if errors:
        print(f"Repository validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"- {error}")
        return 1

    trigger_count = len(json.loads(TRIGGER_CASES.read_text(encoding="utf-8"))["cases"])
    fixture_count = len(REQUIRED_FIXTURES)
    print("Repository validation passed")
    print(f"- skill: {SKILL_DIR.name}")
    print(f"- version: {version}")
    print(f"- trigger cases: {trigger_count}")
    print(f"- fixture files: {fixture_count}")
    print(f"- skill files: {1 + len(REQUIRED_REFERENCES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
