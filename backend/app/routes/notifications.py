from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.notifications import NotificationOut, NotificationTriggerRequest
from app.services.notification_service import list_notifications, trigger_notification
from database.session import get_db

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/trigger", response_model=NotificationOut)
async def trigger(
    payload: NotificationTriggerRequest,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> NotificationOut:
    row = await trigger_notification(db, worker_id=payload.worker_id, channel=payload.channel, message=payload.message)
    return NotificationOut.model_validate(row)


@router.get("/worker/{worker_id}", response_model=list[NotificationOut])
async def worker_notifications(
    worker_id: str,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[NotificationOut]:
    rows = await list_notifications(db, worker_id)
    return [NotificationOut.model_validate(row) for row in rows]
