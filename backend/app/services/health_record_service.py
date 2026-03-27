from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.health_record import HealthRecord
from app.schemas.health_records import HealthRecordCreate, HealthRecordUpdate


async def create_health_record(db: AsyncSession, payload: HealthRecordCreate) -> HealthRecord:
    row = HealthRecord(
        worker_id=payload.worker_id,
        record_type=payload.record_type,
        data_json=payload.data_json,
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row


async def list_worker_health_records(
    db: AsyncSession, worker_id: str, skip: int = 0, limit: int = 100
) -> tuple[list[HealthRecord], int]:
    # Get total count
    count_stmt = select(func.count(HealthRecord.id)).where(HealthRecord.worker_id == worker_id)
    total = await db.scalar(count_stmt)

    # Get paginated records
    stmt = (
        select(HealthRecord)
        .where(HealthRecord.worker_id == worker_id)
        .order_by(desc(HealthRecord.created_at))
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    records = list(result.scalars().all())

    return records, total or 0


async def get_health_record(db: AsyncSession, record_id: str) -> HealthRecord | None:
    return await db.get(HealthRecord, record_id)


async def update_health_record(db: AsyncSession, record: HealthRecord, payload: HealthRecordUpdate) -> HealthRecord:
    if payload.record_type is not None:
        record.record_type = payload.record_type
    if payload.data_json is not None:
        record.data_json = payload.data_json
    await db.commit()
    await db.refresh(record)
    return record


async def delete_health_record(db: AsyncSession, record: HealthRecord) -> None:
    await db.delete(record)
    await db.commit()
