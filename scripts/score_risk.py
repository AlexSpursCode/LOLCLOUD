from __future__ import annotations

from typing import Any, Dict


WEIGHTS = {
    "privilege_required": 0.20,
    "ease_of_abuse": 0.20,
    "impact": 0.30,
    "detection_likelihood": 0.15,
    "evasion_potential": 0.15,
}


def compute_score(risk: Dict[str, Any]) -> float:
    p = int(risk["privilege_required"])
    e = int(risk["ease_of_abuse"])
    i = int(risk["impact"])
    d = int(risk["detection_likelihood"])
    v = int(risk["evasion_potential"])

    raw = (
        WEIGHTS["privilege_required"] * p
        + WEIGHTS["ease_of_abuse"] * e
        + WEIGHTS["impact"] * i
        + WEIGHTS["detection_likelihood"] * (6 - d)
        + WEIGHTS["evasion_potential"] * v
    )
    return round((raw / 5) * 10, 1)


def severity_for_score(score: float) -> str:
    if score <= 2.9:
        return "low"
    if score <= 5.9:
        return "medium"
    if score <= 7.9:
        return "high"
    return "critical"


def apply_risk(entry: Dict[str, Any]) -> Dict[str, Any]:
    risk = dict(entry["risk"])
    score = compute_score(risk)
    risk["score"] = score
    risk["severity"] = severity_for_score(score)
    entry = dict(entry)
    entry["risk"] = risk
    return entry
