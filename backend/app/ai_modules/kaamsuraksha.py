from __future__ import annotations

from typing import Any
from dataclasses import dataclass


@dataclass
class RiskComputationResult:
    silicosis: float
    byssinosis: float
    occupational_asthma: float
    risk_level: str
    predicted_disease: str
    top_factors: list[dict[str, Any]]
    recommendations: list[str]


OCCUPATION_BASE = {
    "stone_quarry": {"silicosis": 0.48, "byssinosis": 0.04, "occupational_asthma": 0.18},
    "construction_worker": {"silicosis": 0.28, "byssinosis": 0.03, "occupational_asthma": 0.14},
    "sandblasting_worker": {"silicosis": 0.52, "byssinosis": 0.02, "occupational_asthma": 0.2},
    "textile_mill_worker": {"silicosis": 0.07, "byssinosis": 0.52, "occupational_asthma": 0.24},
    "garment_worker": {"silicosis": 0.05, "byssinosis": 0.3, "occupational_asthma": 0.16},
    "miner": {"silicosis": 0.4, "byssinosis": 0.03, "occupational_asthma": 0.22},
}

TASK_WEIGHTS = {
    "drilling": {"silicosis": 0.2},
    "stone_cutting": {"silicosis": 0.23},
    "sandblasting": {"silicosis": 0.25},
    "spinning": {"byssinosis": 0.16},
    "weaving": {"byssinosis": 0.12},
    "chemical_mixing": {"occupational_asthma": 0.2},
    "fume_exposure": {"occupational_asthma": 0.18},
}

SYMPTOM_WEIGHTS = {
    "persistent_cough": {"silicosis": 0.12, "byssinosis": 0.07},
    "breathlessness": {"silicosis": 0.1, "byssinosis": 0.11, "occupational_asthma": 0.12},
    "chest_tightness": {"occupational_asthma": 0.13, "byssinosis": 0.06},
    "wheeze": {"occupational_asthma": 0.16},
}

PPE_MULTIPLIER = {
    "always": 0.55,
    "sometimes": 0.82,
    "rarely": 1.18,
    "never": 1.35,
}


def _clamp(value: float, lower: float = 0.0, upper: float = 0.99) -> float:
    return max(lower, min(upper, value))


def _risk_level_from_score(score: float) -> str:
    if score >= 0.7:
        return "HIGH"
    if score >= 0.4:
        return "MEDIUM"
    return "LOW"


def _ml_surrogate_score(
    occupation: str,
    years_in_job: int,
    tasks: list[str],
    ppe_usage: str,
    symptoms: list[str],
    age: int | None,
) -> float:
    score = 0.2
    if occupation in {"stone_quarry", "sandblasting_worker", "miner"}:
        score += 0.25
    score += min(years_in_job / 25, 1.0) * 0.22
    score += min(len(tasks), 5) * 0.05
    score += min(len(symptoms), 4) * 0.06

    if ppe_usage == "rarely":
        score += 0.12
    elif ppe_usage == "never":
        score += 0.17
    elif ppe_usage == "always":
        score -= 0.08

    if age and age > 45:
        score += 0.07
    return _clamp(score)


def _recommendations(predicted_disease: str, risk_level: str) -> list[str]:
    common = [
        "Counsel worker on PPE compliance",
        "Provide regional-language safety guidance",
    ]

    disease_map = {
        "silicosis": [
            "Chest X-ray immediately",
            "Spirometry test",
            "Refer to occupational health specialist",
        ],
        "byssinosis": [
            "Pulmonary function test",
            "Dust exposure reduction plan",
            "Respiratory specialist consultation",
        ],
        "occupational_asthma": [
            "Peak flow monitoring",
            "Bronchodilator response testing",
            "Workplace chemical exposure audit",
        ],
    }

    output = disease_map.get(predicted_disease, ["Clinical screening in nearest PHC"])
    if risk_level == "LOW":
        output = ["Annual occupational screening", "Symptom check every 90 days"]
    if risk_level == "MEDIUM":
        output.append("Follow-up visit within 30 days")
    if risk_level == "HIGH":
        output.append("Priority referral within 72 hours")
    return output + common


def compute_risk_profile(
    occupation: str,
    years_in_job: int,
    tasks: list[str],
    ppe_usage: str,
    symptoms: list[str],
    age: int | None = None,
) -> RiskComputationResult:
    occupation_key = occupation.strip().lower()
    ppe_key = ppe_usage.strip().lower()
    task_keys = [task.strip().lower() for task in tasks]
    symptom_keys = [symptom.strip().lower() for symptom in symptoms]

    base = OCCUPATION_BASE.get(occupation_key, {"silicosis": 0.12, "byssinosis": 0.1, "occupational_asthma": 0.12})

    contributions: dict[str, float] = {}

    silicosis = base["silicosis"]
    byssinosis = base["byssinosis"]
    asthma = base["occupational_asthma"]
    contributions[f"occupation_{occupation_key}"] = max(base.values())  # type: ignore[type-var]

    years_impact = min(years_in_job / 20, 1.0) * 0.24
    silicosis += years_impact * 1.1
    byssinosis += years_impact * 0.7
    asthma += years_impact * 0.65
    contributions["years_in_job"] = round(years_impact, 4)  # type: ignore[call-overload]

    for task in task_keys:
        weights = TASK_WEIGHTS.get(task, {})
        if "silicosis" in weights:
            silicosis += weights["silicosis"]  # type: ignore[operator]
            contributions[f"task_{task}"] = weights["silicosis"]
        if "byssinosis" in weights:
            byssinosis += weights["byssinosis"]  # type: ignore[operator]
            contributions[f"task_{task}"] = weights["byssinosis"]
        if "occupational_asthma" in weights:
            asthma += weights["occupational_asthma"]  # type: ignore[operator]
            contributions[f"task_{task}"] = weights["occupational_asthma"]

    for symptom in symptom_keys:
        weights = SYMPTOM_WEIGHTS.get(symptom, {})
        silicosis += weights.get("silicosis", 0)
        byssinosis += weights.get("byssinosis", 0)
        asthma += weights.get("occupational_asthma", 0)
        if weights:
            contributions[f"symptom_{symptom}"] = max(weights.values())  # type: ignore[type-var]

    ppe_factor = PPE_MULTIPLIER.get(ppe_key, 1.0)
    silicosis *= ppe_factor
    byssinosis *= ppe_factor
    asthma *= ppe_factor

    if ppe_key in {"rarely", "never"}:
        contributions["ppe_usage"] = 0.28 if ppe_key == "rarely" else 0.33
    else:
        contributions["ppe_usage"] = 0.08

    # KaamSuraksha demo fallback rule requested by product brief.
    if occupation_key == "stone_quarry" and years_in_job > 5 and ppe_key in {"rarely", "never"}:
        silicosis = max(silicosis, 0.83)
        contributions["rule_stone_quarry_exposure"] = 0.3

    if age and age > 50:
        silicosis += 0.06
        byssinosis += 0.04
        asthma += 0.05
        contributions["age"] = 0.1

    # Hybrid blend: rule-based domain score + lightweight ML surrogate score.
    ml_score = _ml_surrogate_score(
        occupation=occupation_key,
        years_in_job=years_in_job,
        tasks=task_keys,
        ppe_usage=ppe_key,
        symptoms=symptom_keys,
        age=age,
    )

    silicosis = _clamp((silicosis * 0.7) + (ml_score * 0.3))
    byssinosis = _clamp((byssinosis * 0.78) + (ml_score * 0.22))
    asthma = _clamp((asthma * 0.76) + (ml_score * 0.24))

    disease_scores = {
        "silicosis": silicosis,
        "byssinosis": byssinosis,
        "occupational_asthma": asthma,
    }
    predicted_disease = max(disease_scores, key=disease_scores.get)  # type: ignore[arg-type]
    top_score = disease_scores[predicted_disease]
    risk_level = _risk_level_from_score(top_score)

    contribution_total = sum(contributions.values()) or 1.0

    def format_value(feature: str) -> str:
        if feature == "years_in_job":
            return f"{years_in_job} years"
        if feature.startswith("task_"):
            return "daily"
        if feature.startswith("symptom_"):
            return "reported"
        if feature == "ppe_usage":
            return ppe_key
        if feature == "age":
            return f"{age} years"
        if feature.startswith("occupation_"):
            return occupation_key
        if feature == "rule_stone_quarry_exposure":
            return "high dust exposure"
        return "present"

    top_factors = sorted(  # type: ignore[misc]
        [
            {
                "feature": feature,
                "impact": round(value / contribution_total, 4),  # type: ignore[call-overload]
                "value": format_value(feature),
            }
            for feature, value in contributions.items()
        ],
        key=lambda item: item["impact"],
        reverse=True,
    )[:3]  # type: ignore[index]

    return RiskComputationResult(
        silicosis=round(silicosis, 4),  # type: ignore[call-overload]
        byssinosis=round(byssinosis, 4),  # type: ignore[call-overload]
        occupational_asthma=round(asthma, 4),  # type: ignore[call-overload]
        risk_level=risk_level,
        predicted_disease=predicted_disease,
        top_factors=top_factors,
        recommendations=_recommendations(predicted_disease, risk_level),
    )
