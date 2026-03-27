import logging
from datetime import datetime, timezone

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification
from database.redis_client import redis_client

logger = logging.getLogger(__name__)


async def trigger_notification(db: AsyncSession, worker_id: str, channel: str, message: str) -> Notification:
    row = Notification(
        worker_id=worker_id,
        channel=channel,
        message=message,
        status="sent",
        sent_at=datetime.now(timezone.utc),
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)

    logger.info("Notification sent: worker=%s channel=%s", worker_id, channel)

    if redis_client is not None:
        try:
            await redis_client.rpush(
                "notifications:events",
                f"{row.id}|{worker_id}|{channel}|{message}",
            )
        except Exception:
            logger.warning("Redis notification queue unavailable", exc_info=True)

    return row


async def list_notifications(db: AsyncSession, worker_id: str) -> list[Notification]:
    result = await db.execute(
        select(Notification)
        .where(Notification.worker_id == worker_id)
        .order_by(desc(Notification.created_at))
    )
    return list(result.scalars().all())
