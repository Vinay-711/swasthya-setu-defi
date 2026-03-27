from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.models.risk_profile import RiskProfile
from app.models.user import User
from app.schemas.risk import RiskProfileRequest, RiskProfileResponse
from app.services.risk_service import create_risk_profile, get_latest_worker_risk, list_worker_risks
from database.session import get_db

router = APIRouter(prefix="/occupational", tags=["occupational"])


@router.post("/risk-profile", response_model=RiskProfileResponse)
async def risk_profile(
    payload: RiskProfileRequest,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> RiskProfileResponse:
    profile, scores_json = await create_risk_profile(db, payload)
    return RiskProfileResponse(
        silicosis=scores_json["silicosis"],
        byssinosis=scores_json["byssinosis"],
        occupational_asthma=scores_json["occupational_asthma"],
        risk_level=scores_json["risk_level"],
        predicted_disease=scores_json["predicted_disease"],
        top_factors=scores_json["top_factors"],
        recommendations=scores_json["recommendations"],
    )


@router.get("/risk-profile", response_model=RiskProfileResponse)
async def risk_profile_get(
    worker_id: str,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> RiskProfileResponse:
    latest = await get_latest_worker_risk(db, worker_id)
    if not latest:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No risk profile found")

    scores = latest.scores_json
    return RiskProfileResponse(
        silicosis=float(scores.get("silicosis", 0)),
        byssinosis=float(scores.get("byssinosis", 0)),
        occupational_asthma=float(scores.get("occupational_asthma", 0)),
        risk_level=str(scores.get("risk_level", "LOW")),
        predicted_disease=str(scores.get("predicted_disease", "unknown")),
        top_factors=list(scores.get("top_factors", [])),
        recommendations=list(scores.get("recommendations", [])),
    )


@router.get("/recommendations/{worker_id}")
async def recommendations(
    worker_id: str,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict[str, object]:
    latest = await get_latest_worker_risk(db, worker_id)
    if not latest:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No risk profile found")

    return {
        "worker_id": worker_id,
        "risk_level": latest.risk_level,
        "predicted_disease": latest.scores_json.get("predicted_disease"),
        "recommendations": latest.scores_json.get("recommendations", []),
    }


@router.get("/explain/{risk_id}")
async def explain(
    risk_id: str,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict[str, object]:
    row = await db.get(RiskProfile, risk_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Risk profile not found")

    return {
        "risk_id": row.id,
        "risk_level": row.risk_level,
        "top_factors": row.scores_json.get("top_factors", []),
        "scores": {
            "silicosis": row.scores_json.get("silicosis", 0),
            "byssinosis": row.scores_json.get("byssinosis", 0),
            "occupational_asthma": row.scores_json.get("occupational_asthma", 0),
        },
    }


from typing import Any

@router.get("/history/{worker_id}")
async def history(
    worker_id: str,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[dict[str, Any]]:
    rows = await list_worker_risks(db, worker_id)
    return [
        {
            "id": row.id,
            "occupation": row.occupation,
            "risk_level": row.risk_level,
            "scores_json": row.scores_json,
            "created_at": row.created_at,
        }
        for row in rows
    ]
