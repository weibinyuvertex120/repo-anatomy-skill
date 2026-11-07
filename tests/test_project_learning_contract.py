#!/usr/bin/env python3
"""Validate project-type learning cases and user-run record instances."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "evals/project-learning-cases.json"
SCHEMA_PATH = ROOT / "evals/user-run-record.schema.json"
SKILL_PATH = ROOT / "skills/research-material-writer/SKILL.md"
TYPE_REFERENCE = ROOT / "skills/research-material-writer/references/project-type-profiles.md"
LEARNING_REFERENCE = ROOT / "skills/research-material-writer/references/learning-validation-feedback.md"

EXPECTED_TYPES = {
    "cli_or_local_tool",
    "library_or_sdk",
    "api_or_hosted_service",
    "plugin_or_extension",
    "agent_skill_or_mcp",
    "model",
    "dataset_or_resource_collection",
    "service_application",
}
REQUIRED_CASE_FIELDS = {
    "id",
    "project_type",
    "prompt",
    "required_understanding",
    "required_practice",
    "required_boundary",
    "required_transfer",
}
REQUIRED_SKILL_MARKERS = (
    'version: "0.4.0-preview.1"',
    "project-type-profiles.md",
    "learning-validation-feedback.md",
    "understanding map",
    "practice path",
    "transfer task",
    "guided run",
)
REQUIRED_SCHEMA_FIELDS = {
    "contract",
    "skill_version",
    "project_type",
    "reader_profile",
    "interaction_mode",
    "verification_scope",
    "orientation_check",
    "boundary_check",
    "transfer_task",
    "task_result",
    "feedback",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def type_matches(instance: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(instance, dict)
    if expected == "array":
        return isinstance(instance, list)
    if expected == "string":
        return isinstance(instance, str)
    if expected == "integer":
        return isinstance(instance, int) and not isinstance(instance, bool)
    if expected == "number":
        return isinstance(instance, (int, float)) and not isinstance(instance, bool)
    if expected == "boolean":
        return isinstance(instance, bool)
    if expected == "null":
        return instance is None
    raise AssertionError(f"unsupported schema type in test validator: {expected}")


def resolve_ref(root_schema: dict[str, Any], reference: str) -> dict[str, Any]:
    require(reference.startswith("#/"), f"unsupported non-local schema reference: {reference}")
    current: Any = root_schema
    for token in reference[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        current = current[token]
    require(isinstance(current, dict), f"schema reference does not resolve to an object: {reference}")
    return current


def validation_errors(
    instance: Any,
    schema: dict[str, Any],
    root_schema: dict[str, Any],
    path: str = "$",
) -> list[str]:
    errors: list[str] = []

    reference = schema.get("$ref")
    if isinstance(reference, str):
        errors.extend(validation_errors(instance, resolve_ref(root_schema, reference), root_schema, path))

    expected_type = schema.get("type")
    if isinstance(expected_type, str) and not type_matches(instance, expected_type):
        return [f"{path}: expected {expected_type}"]

    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: value does not match const")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value is not in enum")

    if isinstance(instance, str):
        minimum_length = schema.get("minLength")
        if isinstance(minimum_length, int) and len(instance) < minimum_length:
            errors.append(f"{path}: string is shorter than minLength")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")
        if isinstance(minimum, (int, float)) and instance < minimum:
            errors.append(f"{path}: number is below minimum")
        if isinstance(maximum, (int, float)) and instance > maximum:
            errors.append(f"{path}: number is above maximum")

    if isinstance(instance, dict):
        required = schema.get("required", [])
        if isinstance(required, list):
            for key in required:
                if key not in instance:
                    errors.append(f"{path}: missing required property {key}")
        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            for key, value in instance.items():
                child_schema = properties.get(key)
                if isinstance(child_schema, dict):
                    errors.extend(validation_errors(value, child_schema, root_schema, f"{path}.{key}"))
                elif schema.get("additionalProperties") is False:
                    errors.append(f"{path}: unexpected property {key}")

    if isinstance(instance, list):
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, value in enumerate(instance):
                errors.extend(validation_errors(value, item_schema, root_schema, f"{path}[{index}]"))
        if schema.get("uniqueItems") is True:
            normalized = [json.dumps(value, ensure_ascii=False, sort_keys=True) for value in instance]
            if len(normalized) != len(set(normalized)):
                errors.append(f"{path}: array items are not unique")

    all_of = schema.get("allOf")
    if isinstance(all_of, list):
        for index, sub_schema in enumerate(all_of):
            if isinstance(sub_schema, dict):
                errors.extend(validation_errors(instance, sub_schema, root_schema, f"{path}.allOf[{index}]"))

    if_schema = schema.get("if")
    then_schema = schema.get("then")
    if isinstance(if_schema, dict) and isinstance(then_schema, dict):
        if not validation_errors(instance, if_schema, root_schema, path):
            errors.extend(validation_errors(instance, then_schema, root_schema, path))

    not_schema = schema.get("not")
    if isinstance(not_schema, dict) and not validation_errors(instance, not_schema, root_schema, path):
        errors.append(f"{path}: instance matches prohibited schema")

    any_of = schema.get("anyOf")
    if isinstance(any_of, list):
        matches = [
            not validation_errors(instance, sub_schema, root_schema, path)
            for sub_schema in any_of
            if isinstance(sub_schema, dict)
        ]
        if not any(matches):
            errors.append(f"{path}: instance does not match anyOf")

    return errors


def valid_run_record(**overrides: Any) -> dict[str, Any]:
    record: dict[str, Any] = {
        "contract": "portable-project-learning-v1",
        "skill_version": "0.4.0-preview.1",
        "project_type": "cli_or_local_tool",
        "reader_profile": {
            "role": "developer",
            "experience": "beginner",
            "target_task": "Complete and verify one controlled operation",
        },
        "interaction_mode": "guided_run",
        "verification_scope": {
            "environment": "isolated local fixture",
            "version_scope": "pinned example version",
            "executed": ["first observable success"],
            "blocked_checks": [],
        },
        "orientation_check": {
            "prompt": "Identify the input, processing, and output.",
            "result": "passed",
            "evidence": "Reader identified all three elements.",
        },
        "boundary_check": {
            "prompt": "Trigger one documented failure boundary.",
            "result": "passed",
            "evidence": "The expected refusal was observed.",
        },
        "transfer_task": {
            "prompt": "Change one input and predict the result.",
            "result": "passed",
            "evidence": "Prediction matched the observed result.",
        },
        "task_result": "completed",
        "feedback": [],
    }
    record.update(overrides)
    return record


def require_valid(instance: dict[str, Any], schema: dict[str, Any], label: str) -> None:
    errors = validation_errors(instance, schema, schema)
    require(not errors, f"{label} should be valid, got: {errors}")


def require_invalid(instance: dict[str, Any], schema: dict[str, Any], label: str) -> None:
    errors = validation_errors(instance, schema, schema)
    require(bool(errors), f"{label} should be rejected by the schema")


def main() -> int:
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    require(cases.get("contract") == "portable-project-learning-v1", "unexpected learning contract")
    require(cases.get("version") == "0.4.0-preview.1", "case version mismatch")
    items = cases.get("cases")
    require(isinstance(items, list), "cases must be a list")
    require(len(items) == len(EXPECTED_TYPES), "expected one case for each project type")

    seen_ids: set[str] = set()
    seen_types: set[str] = set()
    for item in items:
        require(isinstance(item, dict), "each case must be an object")
        missing = REQUIRED_CASE_FIELDS - set(item)
        require(not missing, f"case missing fields: {sorted(missing)}")
        case_id = item["id"]
        project_type = item["project_type"]
        require(isinstance(case_id, str) and case_id, "case id must be non-empty")
        require(case_id not in seen_ids, f"duplicate case id: {case_id}")
        require(project_type in EXPECTED_TYPES, f"unknown project type: {project_type}")
        require(project_type not in seen_types, f"duplicate project type: {project_type}")
        understanding = item["required_understanding"]
        require(isinstance(understanding, list) and len(understanding) >= 3, f"{case_id}: insufficient understanding fields")
        require(len(set(understanding)) == len(understanding), f"{case_id}: repeated understanding field")
        for field in ("prompt", "required_practice", "required_boundary", "required_transfer"):
            require(isinstance(item[field], str) and item[field].strip(), f"{case_id}: empty {field}")
        seen_ids.add(case_id)
        seen_types.add(project_type)
    require(seen_types == EXPECTED_TYPES, "project type coverage mismatch")

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "unexpected schema draft")
    require(schema.get("type") == "object", "run record schema must describe an object")
    require(schema.get("additionalProperties") is False, "run record schema must reject unknown fields")
    require(set(schema.get("required", [])) == REQUIRED_SCHEMA_FIELDS, "run record required fields mismatch")
    properties = schema.get("properties", {})
    require(properties.get("contract", {}).get("const") == "portable-project-learning-v1", "schema contract mismatch")
    project_type_ref = properties.get("project_type", {}).get("$ref")
    secondary_type_ref = properties.get("secondary_project_type", {}).get("$ref")
    require(project_type_ref == "#/$defs/projectType", "primary project type must use shared enum")
    require(secondary_type_ref == project_type_ref, "secondary project type must use shared enum")
    project_types = set(resolve_ref(schema, project_type_ref).get("enum", []))
    require(project_types == EXPECTED_TYPES, "schema project type enum mismatch")
    require(set(properties.get("interaction_mode", {}).get("enum", [])) == {"one_shot", "guided_run"}, "interaction modes mismatch")
    require(set(properties.get("task_result", {}).get("enum", [])) == {"completed", "partially_completed", "blocked", "not_verified"}, "task results mismatch")

    require_valid(valid_run_record(), schema, "single-type run record")
    require_valid(
        valid_run_record(secondary_project_type="service_application"),
        schema,
        "distinct primary and secondary type record",
    )
    require_invalid(valid_run_record(project_type="mixed"), schema, "mixed primary type")
    require_invalid(
        valid_run_record(secondary_project_type="unknown_project_type"),
        schema,
        "unknown secondary type",
    )
    require_invalid(
        valid_run_record(secondary_project_type="cli_or_local_tool"),
        schema,
        "identical primary and secondary types",
    )

    require(TYPE_REFERENCE.is_file(), "missing project type reference")
    require(LEARNING_REFERENCE.is_file(), "missing learning validation reference")
    skill_text = SKILL_PATH.read_text(encoding="utf-8")
    lowered = skill_text.lower()
    for marker in REQUIRED_SKILL_MARKERS:
        require(marker.lower() in lowered, f"SKILL.md missing marker: {marker}")

    print("Project learning contract tests passed")
    print(f"- project types: {len(seen_types)}")
    print("- type routing: one primary plus at most one distinct secondary type")
    print("- interaction modes: one_shot, guided_run")
    print("- learning checks: orientation, boundary, transfer")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
