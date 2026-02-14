# LOLCLOUD

LOLCLOUD is a community-driven catalog and investigation framework for cloud-native Living Off the Land (LotL) techniques.

## Why LOLCLOUD

LOLCLOUD was created to address a gap in modern detection engineering: most Living Off the Land references were designed for endpoint binaries, while attackers increasingly abuse cloud-native control planes, identity systems, and service APIs.

Projects like LOLBAS established a strong model for documenting trusted binary abuse on hosts. LOLCLOUD builds beyond that model for cloud environments by cataloging abuse of native cloud primitives across AWS, Azure, and GCP, with provider-specific telemetry requirements, detection guidance, and risk scoring that can be operationalized in SIEM and SOC workflows.

## Phase 1 goals

- Canonical cross-cloud technique schema (`TechniqueEntry v1`)
- YAML catalog for AWS, Azure, and GCP
- Deterministic risk scoring engine
- Telemetry and detection-first guidance for every technique
- CI validation gates and contribution workflow
- Reproducible JSON/NDJSON exports for SIEM and downstream tooling

## Project Organization and Usage

LOLCLOUD uses a source-validate-export lifecycle: update `catalog/`, run `scripts/`, produce `exports/`, and verify with `tests/`.

| Directory | Purpose | How it is used |
|---|---|---|
| `catalog/` | Technique source data | Contributors add/update entries by provider |
| `schemas/` | Structure rules | Validation gates in local checks and CI |
| `taxonomy/` | Shared mappings | Standardizes ATT&CK/category labeling |
| `scripts/` | Automation | Validates entries, computes risk, generates exports |
| `exports/` | Generated outputs | Consumed by SIEM, analytics, and future UI |
| `tests/` | Verification | Ensures schema, scoring, and export correctness |

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
