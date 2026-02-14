from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from scripts.validate_catalog import iter_catalog_files, load_yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "technique.schema.json"


def test_valid_entries_pass_schema() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    files = iter_catalog_files()
    assert files, "expected catalog entries"

    for file in files:
        data = load_yaml(file)
        errors = list(validator.iter_errors(data))
        assert not errors, f"schema validation failed for {file}: {errors[0].message}"


def test_missing_required_telemetry_fails() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    file = iter_catalog_files()[0]
    data = load_yaml(file)
    data["telemetry"]["required_logs"] = []

    errors = list(validator.iter_errors(data))
    assert errors, "expected validation error for missing telemetry.required_logs"


def test_invalid_provider_enum_fails() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    file = iter_catalog_files()[0]
    data = load_yaml(file)
    data["provider"] = "oracle"

    errors = list(validator.iter_errors(data))
    assert errors, "expected validation error for invalid provider"
