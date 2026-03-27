from app.ai_modules.kaamsuraksha import compute_risk_profile


def test_kaamsuraksha_top_factor_ordering():
    result = compute_risk_profile(
        occupation="stone_quarry",
        years_in_job=10,
        tasks=["drilling", "stone_cutting"],
        ppe_usage="rarely",
        symptoms=["persistent_cough"],
        age=45,
    )

    assert result.silicosis > 0.7
    assert len(result.top_factors) == 3
    assert result.top_factors[0]["impact"] >= result.top_factors[1]["impact"]
