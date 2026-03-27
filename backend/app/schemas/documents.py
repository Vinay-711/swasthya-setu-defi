from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    worker_id: str
    original_path: str
    status: str
    parsed_json: dict[str, Any]
    created_at: datetime


class DocumentTranslateRequest(BaseModel):
    target_language: str
