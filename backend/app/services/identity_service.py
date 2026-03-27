from sqlalchemy import desc, select  # pyre-ignore[21]
from sqlalchemy.ext.asyncio import AsyncSession  # pyre-ignore[21]

from app.models.document import Document  # pyre-ignore[21]
from app.models.health_record import HealthRecord  # pyre-ignore[21]
from app.models.notification import Notification  # pyre-ignore[21]
from app.models.risk_profile import RiskProfile  # pyre-ignore[21]
from app.models.user import User, UserRole  # pyre-ignore[21]
from app.schemas.identity import WorkerRecordResponse  # pyre-ignore[21]
from app.utils.ids import generate_swasthya_id  # pyre-ignore[21]
from app.utils.qr import build_qr_data_url  # pyre-ignore[21]


async def create_identity(db: AsyncSession, user_id: str) -> tuple[User, str]:
    user = await db.get(User, user_id)
    if not user:
        raise ValueError("User not found")
    if user.role != UserRole.migrant_worker:
        raise ValueError("SwasthyaID can only be generated for migrant worker users")

    if not user.swasthya_id:
        swasthya_id = generate_swasthya_id()
        while (await db.execute(select(User).where(User.swasthya_id == swasthya_id))).scalar_one_or_none():
            swasthya_id = generate_swasthya_id()
        user.swasthya_id = swasthya_id
        await db.commit()
        await db.refresh(user)

    qr_value = f"/worker/{user.swasthya_id}"
    return user, build_qr_data_url(qr_value)


async def set_worker_consent(db: AsyncSession, swasthya_id: str, consent_granted: bool) -> User | None:
    result = await db.execute(select(User).where(User.swasthya_id == swasthya_id))
    user = result.scalar_one_or_none()
    if not user:
        return None

    user.consent_granted = consent_granted
    await db.commit()
    await db.refresh(user)
    return user


async def get_worker_by_swasthya_id(db: AsyncSession, swasthya_id: str) -> User | None:
    result = await db.execute(select(User).where(User.swasthya_id == swasthya_id))
    return result.scalar_one_or_none()


async def link_worker_abha(db: AsyncSession, swasthya_id: str, abha_number: str) -> User | None:
    worker = await get_worker_by_swasthya_id(db, swasthya_id)
    if not worker:
        return None

    worker.abha_number = abha_number
    await db.commit()
    await db.refresh(worker)
    return worker


async def build_worker_record(db: AsyncSession, swasthya_id: str) -> WorkerRecordResponse | None:
    worker = await get_worker_by_swasthya_id(db, swasthya_id)
    if not worker:
        return None

    health_records = (
        await db.execute(
            select(HealthRecord)
            .where(HealthRecord.worker_id == worker.id)
            .order_by(desc(HealthRecord.created_at))
        )
    ).scalars().all()

    risk_profiles = (
        await db.execute(
            select(RiskProfile)
            .where(RiskProfile.worker_id == worker.id)
            .order_by(desc(RiskProfile.created_at))
        )
    ).scalars().all()

    documents = (
        await db.execute(
            select(Document)
            .where(Document.worker_id == worker.id)
            .order_by(desc(Document.created_at))
        )
    ).scalars().all()

    notifications = (
        await db.execute(
            select(Notification)
            .where(Notification.worker_id == worker.id)
            .order_by(desc(Notification.created_at))
        )
    ).scalars().all()

    return WorkerRecordResponse(
        swasthya_id=worker.swasthya_id or "",
        # pyre-ignore[6]
        worker=worker,
        health_records=list(health_records),
        occupational_risk=list(risk_profiles),
        documents=list(documents),
        notifications=list(notifications),
    )
