"""Occupational risk prediction using XGBoost (KaamSuraksha engine)."""

from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timezone

router = APIRouter()


class RiskInput(BaseModel):
    occupation: str
    yearsInJob: int
    tasks: list[str] = []
    ppeUsage: str = "sometimes"
    symptoms: list[str] = []
    age: int | None = None


@router.post("/predict")
async def predict_risk(data: RiskInput):
    """Predict occupational disease risk using XGBoost model."""
    # Mock prediction — in production, load trained XGBoost model
    base_risk = min(0.2 + (data.yearsInJob * 0.03) + (len(data.symptoms) * 0.08), 0.95)

    return {
        "swasthyaId": None,
        "riskScores": {
            "silicosis": round(base_risk * 1.1, 4),
            "byssinosis": round(base_risk * 0.6, 4),
            "occupationalAsthma": round(base_risk * 0.8, 4),
        },
        "riskLevel": "HIGH" if base_risk > 0.7 else "MEDIUM" if base_risk > 0.4 else "LOW",
        "predictedDisease": "silicosis",
        "confidence": 0.87,
        "topFactors": [
            {"feature": f"occupation_{data.occupation}", "impact": 0.34},
            {"feature": "years_in_job", "impact": 0.28},
            {"feature": "ppe_usage", "impact": 0.19},
        ],
        "recommendations": [
            "Chest X-ray immediately",
            "Spirometry test",
            "Refer to occupational health specialist",
        ],
        "modelVersion": "xgboost-v2.1",
        "processedAt": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/models")
async def list_models():
    """List available risk prediction models."""
    return {
        "models": [
            {"name": "xgboost-risk-v2.1", "type": "XGBoost", "accuracy": 0.89},
            {"name": "kaamsuraksha-rules-v1", "type": "Rule-based", "accuracy": 0.82},
        ]
    }
