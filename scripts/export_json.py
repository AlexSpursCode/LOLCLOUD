from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

try:
    from scripts.score_risk import apply_risk
except ModuleNotFoundError:
    from score_risk import apply_risk

ROOT = Path(__file__).resolve().parents[1]
CATALOG_ROOT = ROOT / "catalog"
EXPORTS_DIR = ROOT / "exports"


def load_yaml(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        return yaml.safe_load(text)
    except ModuleNotFoundError:
        return json.loads(text)


def load_entries() -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    for file in sorted(CATALOG_ROOT.rglob("*.yaml")):
        entry = load_yaml(file)
        entries.append(apply_risk(entry))
    entries.sort(key=lambda item: (item["provider"], item["id"]))
    return entries


def write_exports(entries: List[Dict[str, Any]]) -> None:
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    json_path = EXPORTS_DIR / "techniques.json"
    ndjson_path = EXPORTS_DIR / "techniques.ndjson"

    json_path.write_text(json.dumps(entries, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    ndjson_lines = [json.dumps(entry, sort_keys=True) for entry in entries]
    ndjson_path.write_text("\n".join(ndjson_lines) + "\n", encoding="utf-8")


def main() -> int:
    entries = load_entries()
    write_exports(entries)
    print(f"Exported {len(entries)} entries to exports/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
