from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.auth import RegisterRequest
from app.utils.crypto import encrypt_text, get_phone_hash


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_phone(db: AsyncSession, phone: str) -> User | None:
    phone_hash = get_phone_hash(phone)
    result = await db.execute(select(User).where(User.phone_hash == phone_hash))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: str) -> User | None:
    return await db.get(User, user_id)


async def create_user(db: AsyncSession, payload: RegisterRequest) -> User:
    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role,
        name=payload.name,
        phone_encrypted=encrypt_text(payload.phone),
        phone_hash=get_phone_hash(payload.phone),
        language=payload.language,
        age=payload.age,
        blood_type=payload.blood_type,
        allergies=payload.allergies,
        current_medications=payload.current_medications,
        recent_diagnoses=payload.recent_diagnoses,
        consent_granted=payload.consent_granted,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
