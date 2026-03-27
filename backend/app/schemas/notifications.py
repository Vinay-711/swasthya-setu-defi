from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NotificationTriggerRequest(BaseModel):
    worker_id: str
    channel: str = Field(pattern=r"^(sms|whatsapp|ivr)$")
    message: str = Field(min_length=1, max_length=1000)


class NotificationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    worker_id: str
    channel: str
    message: str
    status: str
    sent_at: datetime | None
    created_at: datetime
