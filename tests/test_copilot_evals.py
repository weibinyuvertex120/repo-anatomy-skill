#!/usr/bin/env python3
"""Regression-test the portable Copilot evaluation validator."""

from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from validate_copilot_evals import (
    CONTRACT_PATH,
    ROOT,
    ValidationError,
    aggregate_runs,
    load_json,
    validate_definitions,
    validate_run,
)


def make_pass_record(case: dict[str, object], run_number: int, cases: dict[str, object], contract: dict[str, object]) -> dict[str, object]:
    event = {
        "sequence": 1,
        "event_type": "final_response",
        "capability": "final_response",
        "native_tool": None,
        "call_id": None,
        "input": None,
        "status": "success",
        "output_ref": "response:final",
        "error": None,
    }
    checkpoints = [
        {
            "checkpoint_id": checkpoint,
            "status": "pass",
            "observation_refs": ["response:final"],
            "notes": "Observed in the normalized run record.",
        }
        for checkpoint in case["required_sequence"]
    ]
    return {
        "schema_version": "1.0.0",
        "suite_id": cases["suite_id"],
        "suite_version": cases["suite_version"],
        "evidence_contract_version": contract["contract_version"],
        "case_id": case["case_id"],
        "run_number": run_number,
        "run_id": f"{case['case_id']}-run-{run_number}",
        "recorded_at": "2026-11-01T00:00:00Z",
        "environment": {
            "host": cases["target"]["host"],
            "surface": cases["target"]["surface"],
            "host_version": "test-host",
            "model": "test-model",
            "adapter_version": "0.1.0",
            "core_version": cases["core_skill"]["version"],
            "permission_profile": cases["target"]["permission_profile"],
            "installed_tools": [],
            "notes": "Synthetic validator fixture.",
        },
        "input": copy.deepcopy(case["input"]),
        "expected_trajectory": {
            "required_sequence": copy.deepcopy(case["required_sequence"]),
            "matching_mode": case["matching_mode"],
        },
        "actual_trajectory": {
            "events": [event],
            "checkpoint_results": checkpoints,
        },
        "tool_evidence": [],
        "evidence_records": [],
        "claim_records": [],
        "final_response": "Synthetic grounded Chinese response.",
        "verdict": {
            "outcome": "pass",
            "primary_reason": None,
            "secondary_reasons": [],
            "trajectory_match": "pass",
            "grounding_status": "pass",
            "boundary_status": "pass",
            "task_completion": "complete",
            "evidence_complete": True,
            "evaluator_notes": "Synthetic pass record.",
        },
    }


def expect_failure(name: str, record: dict[str, object], cases: dict[str, object], contract: dict[str, object], expected: str) -> None:
    try:
        validate_run(record, cases, contract, name)
    except (ValidationError, KeyError, TypeError) as exc:
        if expected not in str(exc):
            raise AssertionError(f"{name}: expected {expected!r}, got {exc!r}") from exc
        print(f"PASS {name}")
        return
    raise AssertionError(f"{name}: validator unexpectedly passed")


def main() -> int:
    cases, contract, _schema = validate_definitions()
    case = cases["cases"][1]
    baseline = make_pass_record(case, 1, cases, contract)
    validate_run(baseline, cases, contract, "baseline")
    print("PASS baseline-run")

    missing_field = copy.deepcopy(baseline)
    del missing_field["verdict"]
    expect_failure("missing-field", missing_field, cases, contract, "missing required field")

    wrong_enum = copy.deepcopy(baseline)
    wrong_enum["verdict"]["outcome"] = "success"
    expect_failure("wrong-enum", wrong_enum, cases, contract, "invalid value")

    version_mismatch = copy.deepcopy(baseline)
    version_mismatch["suite_version"] = "9.9.9"
    expect_failure("version-mismatch", version_mismatch, cases, contract, "suite_version mismatch")

    illegal_capability = copy.deepcopy(baseline)
    illegal_capability["actual_trajectory"]["events"][0]["capability"] = "network_write"
    expect_failure("illegal-capability", illegal_capability, cases, contract, "unknown event capability")

    hidden_boundary_failure = copy.deepcopy(baseline)
    hidden_boundary_failure["actual_trajectory"]["events"][0]["capability"] = "local_write"
    expect_failure("hidden-boundary-failure", hidden_boundary_failure, cases, contract, "requires boundary_failure")

    hidden_grounding_failure = copy.deepcopy(baseline)
    hidden_grounding_failure["verdict"]["grounding_status"] = "fail"
    expect_failure("hidden-grounding-failure", hidden_grounding_failure, cases, contract, "grounding failure cannot be reported as pass")

    incomplete_evidence = copy.deepcopy(baseline)
    incomplete_evidence["verdict"]["evidence_complete"] = False
    expect_failure("incomplete-evidence", incomplete_evidence, cases, contract, "incomplete evidence requires evaluation_failure")

    records = [make_pass_record(case, run_number, cases, contract) for run_number in (1, 2)]
    result = aggregate_runs(records, cases)
    if result[case["case_id"]] != "evaluation_failure":
        raise AssertionError("insufficient-runs: expected evaluation_failure")
    print("PASS insufficient-runs")

    records.append(make_pass_record(case, 3, cases, contract))
    result = aggregate_runs(records, cases)
    if result[case["case_id"]] != "pass":
        raise AssertionError("three-of-three: expected pass")
    print("PASS three-of-three")

    grounding = make_pass_record(case, 3, cases, contract)
    grounding["verdict"].update(
        {
            "outcome": "grounding_failure",
            "primary_reason": "unsupported_material_claim",
            "grounding_status": "fail",
            "task_completion": "failed",
        }
    )
    validate_run(grounding, cases, contract, "grounding-run")
    result = aggregate_runs([records[0], records[1], grounding], cases)
    if result[case["case_id"]] != "grounding_failure":
        raise AssertionError("fatal-grounding: expected grounding_failure")
    print("PASS fatal-grounding")

    boundary = make_pass_record(case, 3, cases, contract)
    boundary["actual_trajectory"]["events"][0]["capability"] = "local_write"
    boundary["verdict"].update(
        {
            "outcome": "boundary_failure",
            "primary_reason": "local_side_effect_attempted",
            "boundary_status": "fail",
            "task_completion": "failed",
        }
    )
    validate_run(boundary, cases, contract, "boundary-run")
    grounding_run_two = copy.deepcopy(grounding)
    grounding_run_two["run_number"] = 2
    grounding_run_two["run_id"] = f"{case['case_id']}-run-2-grounding"
    result = aggregate_runs([records[0], grounding_run_two, boundary], cases)
    if result[case["case_id"]] != "boundary_failure":
        raise AssertionError("fatal-boundary: expected boundary_failure precedence")
    print("PASS fatal-boundary")

    with tempfile.TemporaryDirectory(prefix="copilot-eval-contract-") as temporary:
        copied = Path(temporary) / CONTRACT_PATH.name
        copied.write_text(json.dumps(load_json(CONTRACT_PATH), indent=2) + "\n", encoding="utf-8")
        if not copied.is_file():
            raise AssertionError("contract-copy: expected copied contract")
    print("Copilot evaluation validator tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
