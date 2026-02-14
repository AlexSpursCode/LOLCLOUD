from __future__ import annotations

import json
from pathlib import Path

from scripts.export_json import load_entries
from scripts.validate_catalog import iter_catalog_files

ROOT = Path(__file__).resolve().parents[1]


def test_export_count_matches_catalog() -> None:
    entries = load_entries()
    assert len(entries) == len(iter_catalog_files())


def test_ndjson_count_matches_json_export() -> None:
    json_path = ROOT / "exports" / "techniques.json"
    ndjson_path = ROOT / "exports" / "techniques.ndjson"

    json_entries = json.loads(json_path.read_text(encoding="utf-8"))
    ndjson_lines = [line for line in ndjson_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    assert len(json_entries) == len(ndjson_lines)


def test_timestamps_iso_format() -> None:
    entries = load_entries()
    for item in entries:
        assert item["created_at"].endswith("Z")
        assert item["updated_at"].endswith("Z")
