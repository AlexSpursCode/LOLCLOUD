# LOLCLOUD

LOLCLOUD is a community-driven catalog and investigation framework for cloud-native Living Off the Land (LotL) techniques.

## Phase 1 goals

- Canonical cross-cloud technique schema (`TechniqueEntry v1`)
- YAML catalog for AWS, Azure, and GCP
- Deterministic risk scoring engine
- Telemetry and detection-first guidance for every technique
- CI validation gates and contribution workflow
- Reproducible JSON/NDJSON exports for SIEM and downstream tooling

## Project structure

- `catalog/`: Technique entries organized by provider
- `schemas/`: JSON Schemas for technique entries and taxonomy
- `taxonomy/`: Shared ATT&CK tactic/taxonomy references
- `scripts/`: Validation, scoring, and export tooling
- `exports/`: Machine-readable artifacts generated from catalog
- `tests/`: Unit tests for schema, scoring, and export integrity

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/validate_catalog.py
python scripts/export_json.py
pytest -q
```

## Risk scoring model

```text
raw = 0.20*p + 0.20*e + 0.30*i + 0.15*(6-d) + 0.15*v
score = round((raw / 5) * 10, 1)
```

Severity mapping:

- `0.0-2.9`: low
- `3.0-5.9`: medium
- `6.0-7.9`: high
- `8.0-10.0`: critical

## Release target

`v0.1.0` freezes `TechniqueEntry v1` and ships validated seed content with reproducible exports.
