#!/usr/bin/env python3
"""Regression-test the repository validator against intentionally broken copies."""

from __future__ import annotations

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
    path = repository / "evals/trigger-cases.json"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace('"version": "0.1.0"', '"version": "9.9.9"', 1), encoding="utf-8")


def corrupt_json(repository: Path) -> None:
    (repository / "evals/trigger-cases.json").write_text("{invalid json\n", encoding="utf-8")


def main() -> int:
    baseline = run_validator(ROOT)
    if baseline.returncode != 0:
        print(baseline.stdout, end="")
        print(baseline.stderr, end="", file=sys.stderr)
        raise AssertionError("baseline repository must pass before mutation tests")
    print("PASS baseline")

    expect_failure("missing-reference", remove_reference, "Missing skill reference")
    expect_failure("version-mismatch", mismatch_version, "version does not match")
    expect_failure("invalid-json", corrupt_json, "invalid JSON")
    print("Validator regression tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
