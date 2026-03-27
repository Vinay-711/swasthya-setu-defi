from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai_modules.kaamsuraksha import compute_risk_profile
from app.models.risk_profile import RiskProfile
from app.schemas.risk import RiskProfileRequest


async def create_risk_profile(db: AsyncSession, payload: RiskProfileRequest) -> tuple[RiskProfile, dict]:
    result = compute_risk_profile(
        occupation=payload.occupation,
        years_in_job=payload.years_in_job,
        tasks=payload.tasks,
        ppe_usage=payload.ppe_usage,
        symptoms=payload.symptoms,
        age=payload.age,
    )

    scores_json = {
        "silicosis": result.silicosis,
        "byssinosis": result.byssinosis,
        "occupational_asthma": result.occupational_asthma,
        "predicted_disease": result.predicted_disease,
        "risk_level": result.risk_level,
        "top_factors": result.top_factors,
        "recommendations": result.recommendations,
    }

    row = RiskProfile(
        worker_id=payload.worker_id,
        occupation=payload.occupation,
        tasks_json=payload.tasks,
        symptoms_json=payload.symptoms,
        years_in_job=payload.years_in_job,
        scores_json=scores_json,
        risk_level=result.risk_level,
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row, scores_json


async def get_latest_worker_risk(db: AsyncSession, worker_id: str) -> RiskProfile | None:
    result = await db.execute(
        select(RiskProfile)
        .where(RiskProfile.worker_id == worker_id)
        .order_by(desc(RiskProfile.created_at))
        .limit(1)
    )
    return result.scalar_one_or_none()


async def list_worker_risks(db: AsyncSession, worker_id: str) -> list[RiskProfile]:
    result = await db.execute(
        select(RiskProfile)
        .where(RiskProfile.worker_id == worker_id)
        .order_by(desc(RiskProfile.created_at))
    )
    return list(result.scalars().all())
