from scripts.score_risk import compute_score, severity_for_score


def test_risk_score_deterministic() -> None:
    risk = {
        "privilege_required": 4,
        "ease_of_abuse": 4,
        "impact": 5,
        "detection_likelihood": 2,
        "evasion_potential": 4,
    }
    assert compute_score(risk) == compute_score(risk)


def test_severity_boundaries() -> None:
    assert severity_for_score(2.9) == "low"
    assert severity_for_score(3.0) == "medium"
    assert severity_for_score(5.9) == "medium"
    assert severity_for_score(6.0) == "high"
    assert severity_for_score(7.9) == "high"
    assert severity_for_score(8.0) == "critical"
