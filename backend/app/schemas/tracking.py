from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LocationUpdateRequest(BaseModel):
    worker_id: str
    state: str
    city: str
    latitude: str | None = None
    longitude: str | None = None


class LocationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    worker_id: str
    state: str
    city: str
    latitude: str | None
    longitude: str | None
    source: str
    created_at: datetime
