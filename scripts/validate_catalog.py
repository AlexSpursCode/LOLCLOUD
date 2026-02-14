from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

from jsonschema import Draft202012Validator, FormatChecker

try:
    from scripts.score_risk import compute_score, severity_for_score
except ModuleNotFoundError:
    from score_risk import compute_score, severity_for_score

ROOT = Path(__file__).resolve().parents[1]
CATALOG_ROOT = ROOT / "catalog"
SCHEMA_PATH = ROOT / "schemas" / "technique.schema.json"


def load_yaml(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        return yaml.safe_load(text)
    except ModuleNotFoundError:
        return json.loads(text)


def iter_catalog_files() -> List[Path]:
    return sorted(CATALOG_ROOT.rglob("*.yaml"))


def validate_entry(path: Path, validator: Draft202012Validator) -> Dict[str, Any]:
    data = load_yaml(path)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    if errors:
        messages = [f"{path}: {error.message}" for error in errors]
        raise ValueError("\n".join(messages))

    if data["id"].split("-")[1] != data["provider"]:
        raise ValueError(f"{path}: id provider segment must match provider field")

    expected_score = compute_score(data["risk"])
    expected_severity = severity_for_score(expected_score)
    if data["risk"]["score"] != expected_score:
        raise ValueError(
            f"{path}: risk.score mismatch expected {expected_score} got {data['risk']['score']}"
        )
    if data["risk"]["severity"] != expected_severity:
        raise ValueError(
            f"{path}: risk.severity mismatch expected {expected_severity} got {data['risk']['severity']}"
        )

    if len(data["telemetry"]["required_logs"]) < 2:
        raise ValueError(f"{path}: telemetry.required_logs must include at least 2 items")
    if len(data["detection"]["hypotheses"]) < 2:
        raise ValueError(f"{path}: detection.hypotheses must include at least 2 items")
    if len(data["detection"]["false_positive_considerations"]) < 2:
        raise ValueError(
            f"{path}: detection.false_positive_considerations must include at least 2 items"
        )
    if len(data["mitigation"]) < 2:
        raise ValueError(f"{path}: mitigation must include at least 2 items")

    for ref in data["references"]:
        if not re.match(r"^https?://", ref):
            raise ValueError(f"{path}: reference must be http(s) URL: {ref}")

    return data


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    files = iter_catalog_files()
    if not files:
        raise SystemExit("No catalog entries found")

    seen_ids = set()
    entries = []
    for file in files:
        entry = validate_entry(file, validator)
        if entry["id"] in seen_ids:
            raise ValueError(f"Duplicate id detected: {entry['id']}")
        seen_ids.add(entry["id"])
        entries.append(entry)

    print(f"Validated {len(entries)} catalog entries with no errors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
