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

## Project structure

- `catalog/`: Technique entries organized by provider
- `schemas/`: JSON Schemas for technique entries and taxonomy
- `taxonomy/`: Shared ATT&CK tactic/taxonomy references
- `scripts/`: Validation, scoring, and export tooling
- `exports/`: Machine-readable artifacts generated from catalog
- `tests/`: Unit tests for schema, scoring, and export integrity

## How the Project Is Organized

LOLCLOUD follows a source-validate-export workflow:

1. Add or update techniques in `catalog/`
2. Validate and score using `scripts/`
3. Generate artifacts in `exports/`
4. Verify behavior with `tests/`

### `catalog/` (Source of truth)

Provider-specific YAML entries that define cloud LotL techniques and detection guidance.

### `schemas/` (Contract)

Schema definitions that every entry must satisfy.
Used by validation scripts and CI to block malformed contributions.

### `taxonomy/` (Normalization)

Shared tactic/category mapping references used to standardize labels and ATT&CK alignment.

### `scripts/` (Toolchain)

Automation for:
- schema and content validation
- deterministic risk scoring
- reproducible export generation

### `exports/` (Distribution format)

Generated JSON/NDJSON outputs intended for integration with SIEM, analytics pipelines, and external consumers.

### `tests/` (Quality assurance)

Unit tests that confirm:
- valid entries pass
- invalid patterns fail
- risk scoring is deterministic
- export counts and formats remain correct

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
