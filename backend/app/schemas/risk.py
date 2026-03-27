from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TopFactor(BaseModel):
    feature: str
    impact: float
    value: str


class RiskProfileRequest(BaseModel):
    worker_id: str
    occupation: str
    # pyre-ignore[6]
    years_in_job: int = Field(ge=0, le=60)
    tasks: list[str] = Field(default_factory=list)
    ppe_usage: str
    symptoms: list[str] = Field(default_factory=list)
    age: int | None = None


class RiskProfileResponse(BaseModel):
    silicosis: float
    byssinosis: float
    occupational_asthma: float
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
    predicted_disease: str
    top_factors: list[TopFactor]
    recommendations: list[str]


class RiskProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    worker_id: str
    occupation: str
    years_in_job: int
    risk_level: str
    scores_json: dict
    created_at: datetime
