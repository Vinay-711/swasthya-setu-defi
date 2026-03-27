from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.location_log import LocationLog
from app.models.user import User
from app.schemas.tracking import LocationUpdateRequest


async def create_location_log(db: AsyncSession, payload: LocationUpdateRequest) -> LocationLog:
    row = LocationLog(
        worker_id=payload.worker_id,
        state=payload.state,
        city=payload.city,
        latitude=payload.latitude,
        longitude=payload.longitude,
        source="manual",
    )
    db.add(row)

    worker = await db.get(User, payload.worker_id)
    if worker:
        worker.state = payload.state

    await db.commit()
    await db.refresh(row)
    return row


async def list_worker_locations(db: AsyncSession, worker_id: str) -> list[LocationLog]:
    result = await db.execute(
        select(LocationLog)
        .where(LocationLog.worker_id == worker_id)
        .order_by(desc(LocationLog.created_at))
    )
    return list(result.scalars().all())
