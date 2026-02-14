# Contributing to LOLCLOUD

## Workflow

1. Open an issue or choose an existing issue.
2. Add or update entries under `catalog/<provider>/`.
3. Run validation and tests locally.
4. Open a PR using the template.

## Entry quality requirements

Every technique entry must include:

- ATT&CK mappings with rationale
- Required telemetry and minimum configuration
- At least two detection hypotheses
- False-positive considerations
- Risk factors with computed score/severity
- At least two mitigations

## Local checks

```bash
python scripts/validate_catalog.py
python scripts/export_json.py
pytest -q
```
