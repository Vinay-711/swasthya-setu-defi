from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field  # pyre-ignore[21]


class IdentityCreateRequest(BaseModel):
    user_id: str = Field(min_length=1)


class IdentityCreateResponse(BaseModel):
    swasthya_id: str
    worker_id: str
    qr_data_url: str


class ConsentUpdateRequest(BaseModel):
    consent_granted: bool


class LinkABHARequest(BaseModel):
    abha_number: str = Field(min_length=14, max_length=14, pattern=r"^\d{14}$")


class WorkerClinicProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    swasthya_id: str | None
    abha_number: str | None
    name: str
    age: int | None
    blood_type: str | None
    allergies: list[str]
    current_medications: list[str]
    recent_diagnoses: list[str]
    language: str
    state: str | None
    consent_granted: bool
    created_at: datetime


class HealthRecordItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    record_type: str
    data_json: dict[str, Any]
    created_at: datetime


class RiskItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    risk_level: str
    scores_json: dict[str, Any]
    created_at: datetime


class DocumentItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    original_path: str
    parsed_json: dict[str, Any]
    status: str
    created_at: datetime


class NotificationItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    channel: str
    message: str
    status: str
    sent_at: datetime | None
    created_at: datetime


class WorkerRecordResponse(BaseModel):
    swasthya_id: str
    worker: WorkerClinicProfile
    health_records: list[HealthRecordItem]
    occupational_risk: list[RiskItem]
    documents: list[DocumentItem]
    notifications: list[NotificationItem]
