#!/usr/bin/env python3
"""Regression-test the repository validator against intentionally broken copies."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = Path("tests/validate_repository.py")


def run_validator(repository: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(repository / VALIDATOR)],
        cwd=repository,
        env={"PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True,
        text=True,
        check=False,
    )


def copy_repository(destination: Path) -> None:
    shutil.copytree(
        ROOT,
        destination,
        ignore=shutil.ignore_patterns(".git", "dist", "__pycache__", "*.pyc"),
    )


def expect_failure(name: str, mutate, expected_text: str) -> None:
    with tempfile.TemporaryDirectory(prefix=f"wfm-validator-{name}-") as temporary:
        repository = Path(temporary) / "repository"
        copy_repository(repository)
        mutate(repository)
        result = run_validator(repository)
        if result.returncode == 0:
            raise AssertionError(f"{name}: validator unexpectedly passed")
        output = result.stdout + result.stderr
        if expected_text not in output:
            raise AssertionError(
                f"{name}: expected {expected_text!r} in validator output, got:\n{output}"
            )
        print(f"PASS {name}")


def remove_reference(repository: Path) -> None:
    (repository / "skills/workspace-file-maintainer/references/workflow.md").unlink()


def mismatch_version(repository: Path) -> None:
    path = repository / "evals/research-trigger-cases.json"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace('"version": "0.2.0-preview.1"', '"version": "9.9.9"', 1), encoding="utf-8")


def corrupt_json(repository: Path) -> None:
    (repository / "evals/trigger-cases.json").write_text("{invalid json\n", encoding="utf-8")


def mutate_case(repository: Path, **changes: object) -> None:
    path = repository / "evals/research-trigger-cases.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["cases"][0].update(changes)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def empty_prompt(repository: Path) -> None:
    mutate_case(repository, prompt="   ")


def wrong_expected_skill_type(repository: Path) -> None:
    mutate_case(repository, expected_skill="yes")


def unknown_group(repository: Path) -> None:
    mutate_case(repository, group="typo")


def empty_expected_behavior(repository: Path) -> None:
    mutate_case(repository, expected_behavior="")


def duplicate_prompt(repository: Path) -> None:
    path = repository / "evals/research-trigger-cases.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["cases"][1]["prompt"] = data["cases"][0]["prompt"]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def replace_reference_with_symlink(repository: Path) -> None:
    outside = repository.parent / "external-reference.md"
    outside.write_text("external marker", encoding="utf-8")
    reference = repository / "skills/research-material-writer/references/quality-checklist.md"
    reference.unlink()
    reference.symlink_to(outside)


def empty_functional_cases(repository: Path) -> None:
    (repository / "evals/research-functional-cases.md").write_text("\n", encoding="utf-8")


def main() -> int:
    baseline = run_validator(ROOT)
    if baseline.returncode != 0:
        print(baseline.stdout, end="")
        print(baseline.stderr, end="", file=sys.stderr)
        raise AssertionError("baseline repository must pass before mutation tests")
    print("PASS baseline")

    expect_failure("missing-reference", remove_reference, "Missing skill resource")
    expect_failure("version-mismatch", mismatch_version, "version does not match")
    expect_failure("invalid-json", corrupt_json, "invalid JSON")
    expect_failure("empty-prompt", empty_prompt, "prompt must be a non-empty string")
    expect_failure("wrong-expected-skill-type", wrong_expected_skill_type, "expected_skill must be a boolean")
    expect_failure("unknown-group", unknown_group, "unknown group")
    expect_failure("empty-expected-behavior", empty_expected_behavior, "expected_behavior must be a non-empty string")
    expect_failure("duplicate-prompt", duplicate_prompt, "duplicate prompt")
    expect_failure("external-symlink", replace_reference_with_symlink, "symlink is not allowed")
    expect_failure("empty-functional-cases", empty_functional_cases, "missing required section")
    print("Validator regression tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
