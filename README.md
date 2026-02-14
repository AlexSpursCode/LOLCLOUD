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

## Operational Integration by Role

### Security Engineers

#### CI/CD integration

1. In your application repository, pull LOLCLOUD as a submodule or pipeline artifact source.
2. Add a validation stage that runs:

```bash
cd /Users/alejandroaucestovar/Desktop/LOLCLOUD
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/validate_catalog.py
python scripts/export_json.py
pytest -q
```

3. Configure the pipeline to fail if validation, export generation, or tests fail.
4. Publish `exports/techniques.json` as a build artifact for downstream security tooling.
5. Add a scheduled pipeline to diff previous vs current exports and open tickets for new or changed high-risk entries.

#### SIEM integration

1. Create a scheduled ingestion job (for example, daily) for `exports/techniques.ndjson`.
2. Map key fields (`id`, `provider`, `attack_category`, `risk.score`, `risk.severity`, `mitre_attack`) into normalized SIEM fields.
3. Build lookup tables keyed by LOLCLOUD `id`.
4. Translate `detection.analytics` guidance into native SIEM queries.
5. Correlate cloud audit events with LOLCLOUD IDs to enrich alerts with severity and mitigation context.

#### Detection and incident response integration

1. Store one detection-as-code rule per relevant catalog entry.
2. Tag each rule with LOLCLOUD ID, ATT&CK technique ID, provider, and severity.
3. Pass `technique_id`, `mitigation`, and `references` into SOAR cases.
4. Require analysts to execute and document mitigation guidance from the matched entry.
5. Measure MTTD/MTTR by LOLCLOUD ID to prioritize engineering backlog.

### Security Auditors

#### CI/CD integration for control evidence

1. Add an audit evidence pipeline that runs `python scripts/validate_catalog.py`.
2. Require each control test to map to one or more LOLCLOUD IDs.
3. Generate a control coverage report showing mapped vs unmapped techniques.
4. Block release sign-off if critical techniques do not have mapped detective or preventive controls.

#### SIEM integration for telemetry assurance

1. Import `exports/techniques.json` into your GRC or audit evidence store.
2. For each technique, verify required logs listed in `telemetry.required_logs` are present in SIEM.
3. Validate retention against `telemetry.retention_recommendation_days`.
4. Produce a monthly evidence package mapping each technique to proof-of-log and proof-of-detection.
5. File findings for missing logs, missing detections, or weak tuning.

#### Detection and incident response audit checks

1. Select sampled techniques each quarter across all providers.
2. Execute tabletop or simulation scenarios and validate alert generation.
3. Confirm cases include correct LOLCLOUD ID and response actions.
4. Score pass/fail by technique and record gaps in the risk register.

### Security Leadership (CISO / Security Director)

#### CI/CD governance controls

1. Require LOLCLOUD validation to pass before production deployment approval.
2. Require owner assignment and remediation plan for newly introduced critical-risk techniques.
3. Review weekly pipeline summaries for validation failures and critical deltas.

#### SIEM and risk dashboard integration

1. Build dashboards combining LOLCLOUD exports with live detection metrics.
2. Track coverage by provider and attack category.
3. Track KPI trends:
   - Percent of techniques with active detections
   - Percent with tested IR playbooks
   - Count of open critical gaps
4. Use trend data to drive budget and staffing priorities.

#### Detection and incident response operating model

1. Assign accountable owners for each attack category.
2. Require post-incident reviews to map incidents to LOLCLOUD technique IDs.
3. Enforce remediation SLA tiers based on severity.
4. Run quarterly maturity reviews using LOLCLOUD as the baseline framework.

## Release target

`v0.1.0` freezes `TechniqueEntry v1` and ships validated seed content with reproducible exports.
