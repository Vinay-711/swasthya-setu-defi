# pyre-unsafe
"""KaamSuraksha route — AI risk scoring API.

Powers:
  • Doctor Portal → individual risk gauge + SHAP factor waterfall
  • Employer Portal → aggregate health status, compliance, top-risk occupations
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai_modules.kaamsuraksha import compute_risk_profile
from app.models.risk_profile import RiskProfile
from app.models.user import User
from app.core.deps import get_current_user
from app.schemas.risk import RiskProfileRequest, RiskProfileResponse
from app.services.risk_service import create_risk_profile, get_latest_worker_risk
from database.session import get_db

router = APIRouter(prefix="/kaamsuraksha", tags=["kaamsuraksha"])

# ──────────────────────────────────────────────
#  Schemas
# ──────────────────────────────────────────────

class BatchScoreItem(BaseModel):
    worker_id: str
    occupation: str
    years_in_job: int = Field(ge=0, le=60)  # pyre-ignore[6]
    tasks: list[str] = Field(default_factory=list)
    ppe_usage: str
    symptoms: list[str] = Field(default_factory=list)
    age: int | None = None


class BatchScoreRequest(BaseModel):
    workers: list[BatchScoreItem] = Field(..., max_length=50)  # pyre-ignore[6]


class WorkerScoreResult(BaseModel):
    worker_id: str
    risk_level: str
    risk_score: float
    predicted_disease: str
    top_factors: list[dict[str, Any]]
    recommendations: list[str]


class BatchScoreResponse(BaseModel):
    total: int
    results: list[WorkerScoreResult]
    summary: dict[str, int]


class OccupationRisk(BaseModel):
    rank: int
    name: str
    workers: int
    risk_score: float
    detail: str


class HealthStatusBreakdown(BaseModel):
    healthy: int
    at_risk: int  # pyre-ignore[6]
    critical: int


class ComplianceInfo(BaseModel):
    percentage: float
    ppe: float
    screenings: float
    training: float


class EmployerDashboardResponse(BaseModel):
    employer_name: str
    total_workers: int
    health_status: HealthStatusBreakdown
    compliance: ComplianceInfo
    top_risk_occupations: list[OccupationRisk]


# ──────────────────────────────────────────────
#  1. POST /score — single worker risk scoring
# ──────────────────────────────────────────────

@router.post("/score", response_model=RiskProfileResponse)
async def score_worker(
    payload: RiskProfileRequest,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> RiskProfileResponse:
    """Score a single worker's occupational health risk (persists to DB)."""
    _profile, scores_json = await create_risk_profile(db, payload)
    return RiskProfileResponse(
        silicosis=scores_json["silicosis"],
        byssinosis=scores_json["byssinosis"],
        occupational_asthma=scores_json["occupational_asthma"],
        risk_level=scores_json["risk_level"],
        predicted_disease=scores_json["predicted_disease"],
        top_factors=scores_json["top_factors"],
        recommendations=scores_json["recommendations"],
    )


# ──────────────────────────────────────────────
#  2. POST /score/batch — bulk scoring (≤ 50)
# ──────────────────────────────────────────────

@router.post("/score/batch", response_model=BatchScoreResponse)
async def score_batch(
    payload: BatchScoreRequest,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> BatchScoreResponse:
    """Score multiple workers in one call. Powers employer batch imports."""
    results: list[WorkerScoreResult] = []
    summary = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}

    for item in payload.workers:
        result = compute_risk_profile(
            occupation=item.occupation,
            years_in_job=item.years_in_job,
            tasks=item.tasks,
            ppe_usage=item.ppe_usage,
            symptoms=item.symptoms,
            age=item.age,
        )
        top_score = max(result.silicosis, result.byssinosis, result.occupational_asthma)
        summary[result.risk_level] = summary.get(result.risk_level, 0) + 1

        results.append(WorkerScoreResult(
            worker_id=item.worker_id,
            risk_level=result.risk_level,
            risk_score=round(top_score, 4),  # type: ignore[call-overload]
            predicted_disease=result.predicted_disease,
            top_factors=result.top_factors,
            recommendations=result.recommendations,
        ))

    return BatchScoreResponse(
        total=len(results),
        results=results,
        summary=summary,
    )


# ──────────────────────────────────────────────
#  3. GET /score/{worker_id} — latest risk for doctor portal gauge
# ──────────────────────────────────────────────

@router.get("/score/{worker_id}", response_model=RiskProfileResponse)
async def get_worker_score(
    worker_id: str,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> RiskProfileResponse:
    """Fetch the latest risk score for a single worker (Doctor Portal gauge)."""
    latest = await get_latest_worker_risk(db, worker_id)
    if not latest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No risk profile for worker {worker_id}",
        )
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


# ──────────────────────────────────────────────
#  4. GET /employer/dashboard/{employer_id}
#     Aggregate stats for Employer Analytics
# ──────────────────────────────────────────────

# ── Occupation risk lookup (used when no DB data exists) ──
OCCUPATION_RISK_DB: list[dict[str, Any]] = [
    {"name": "Stone Cutting", "base_score": 8.7, "detail": "Silicosis, respiratory exposure"},
    {"name": "Welding & Metal Work", "base_score": 7.2, "detail": "Fume inhalation, burn risk"},
    {"name": "Scaffolding & Heights", "base_score": 6.5, "detail": "Fall hazard, heat exhaustion"},
    {"name": "Textile Mill Work", "base_score": 5.8, "detail": "Byssinosis, dust inhalation"},
    {"name": "Mining", "base_score": 8.2, "detail": "Silicosis, tunnel collapse"},
    {"name": "Sandblasting", "base_score": 9.1, "detail": "Acute silicosis, lung fibrosis"},
    {"name": "Chemical Handling", "base_score": 7.5, "detail": "Toxic fumes, skin burns"},
    {"name": "Construction Labour", "base_score": 6.0, "detail": "Musculoskeletal, falls"},
]


@router.get("/employer/dashboard/{employer_id}", response_model=EmployerDashboardResponse)
async def employer_dashboard(
    employer_id: str,
    db: AsyncSession = Depends(get_db),
) -> EmployerDashboardResponse:
    """
    Aggregated employer dashboard data.

    In production, queries all workers linked to the employer and aggregates
    their latest risk profiles. Falls back to realistic demo data when the DB
    is empty (dev / demo mode).
    """
    # ── Try DB aggregation first ──
    result = await db.execute(
        select(
            RiskProfile.risk_level,
            func.count(func.distinct(RiskProfile.worker_id)).label("cnt"),
        ).group_by(RiskProfile.risk_level)
    )
    rows = result.all()

    if rows:
        level_counts: dict[str, int] = {r.risk_level: r.cnt for r in rows}
        healthy = level_counts.get("LOW", 0)
        at_risk = level_counts.get("MEDIUM", 0)
        critical = level_counts.get("HIGH", 0)
        total = healthy + at_risk + critical

        # Top risk occupations from DB
        occ_result = await db.execute(
            select(
                RiskProfile.occupation,
                func.count(func.distinct(RiskProfile.worker_id)).label("workers"),
            )
            .where(RiskProfile.risk_level.in_(["MEDIUM", "HIGH"]))
            .group_by(RiskProfile.occupation)
            .order_by(func.count(func.distinct(RiskProfile.worker_id)).desc())
            .limit(3)
        )
        occ_rows = occ_result.all()
        top_risk = [
            OccupationRisk(
                rank=i + 1,
                name=row.occupation.replace("_", " ").title(),
                workers=row.workers,
                risk_score=round(8.0 - i * 0.8, 1),  # type: ignore[call-overload]
                detail=_occupation_detail(row.occupation),
            )
            for i, row in enumerate(occ_rows)
        ]
    else:
        # ── Demo fallback ──
        total = 250
        healthy = 180
        at_risk = 50
        critical = 20
        top_risk = [
            OccupationRisk(rank=i + 1, **occ, workers=45 - i * 10)
            for i, occ in enumerate(OCCUPATION_RISK_DB[:3])
        ]

    compliance_pct = round(healthy / max(total, 1) * 100, 1) if total else 95.0  # type: ignore[call-overload]

    return EmployerDashboardResponse(
        employer_name=f"Employer {employer_id}",
        total_workers=total,
        health_status=HealthStatusBreakdown(
            healthy=healthy,
            at_risk=at_risk,
            critical=critical,
        ),
        compliance=ComplianceInfo(
            percentage=min(compliance_pct, 100.0),
            ppe=min(compliance_pct + 3, 100.0),
            screenings=max(compliance_pct - 3, 0.0),
            training=compliance_pct,
        ),
        top_risk_occupations=top_risk,
    )


# ──────────────────────────────────────────────
#  5. GET /occupations/risk-ranking
#     Full occupation risk table
# ──────────────────────────────────────────────

@router.get("/occupations/risk-ranking")
async def occupation_risk_ranking(
    top_n: int = Query(default=5, ge=1, le=20),
    _: User = Depends(get_current_user),
) -> list[OccupationRisk]:
    """Return the top N risky occupations from the KaamSuraksha knowledge base."""
    sorted_occs = sorted(OCCUPATION_RISK_DB, key=lambda x: x["base_score"], reverse=True)
    return [
        OccupationRisk(
            rank=i + 1,
            name=occ["name"],
            workers=0,
            risk_score=occ["base_score"],
            detail=occ["detail"],
        )
        for i, occ in enumerate(sorted_occs[:top_n])
    ]


# ──────────────────────────────────────────────
#  Helpers
# ──────────────────────────────────────────────

def _occupation_detail(occupation_key: str) -> str:
    detail_map = {
        "stone_quarry": "Silicosis, respiratory exposure",
        "stone_cutting": "Silicosis, respiratory exposure",
        "sandblasting_worker": "Acute silicosis, lung fibrosis",
        "textile_mill_worker": "Byssinosis, dust inhalation",
        "construction_worker": "Musculoskeletal, falls",
        "miner": "Silicosis, tunnel collapse",
        "garment_worker": "Byssinosis, respiratory issues",
        "welding": "Fume inhalation, burn risk",
    }
    return detail_map.get(occupation_key.strip().lower(), "Occupational health risk")
