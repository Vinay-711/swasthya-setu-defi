from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class HealthRecordCreate(BaseModel):
    worker_id: str
    record_type: str = Field(min_length=2, max_length=64)
    data_json: dict[str, Any]


class HealthRecordUpdate(BaseModel):
    record_type: str | None = Field(default=None, min_length=2, max_length=64)
    data_json: dict[str, Any] | None = None


class HealthRecordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    worker_id: str
    record_type: str
    data_json: dict[str, Any]
    created_at: datetime
    updated_at: datetime


class HealthRecordListResponse(BaseModel):
    items: list[HealthRecordOut]
    total: int
    skip: int
    limit: int
