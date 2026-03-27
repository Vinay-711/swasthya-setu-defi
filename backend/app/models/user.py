from __future__ import annotations

import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, JSON, String, func  # pyre-ignore[21]
from sqlalchemy.orm import Mapped, mapped_column, relationship  # pyre-ignore[21]

from database.base import Base  # pyre-ignore[21]


class UserRole(str, enum.Enum):
    admin = "admin"
    doctor = "doctor"
    asha_worker = "asha_worker"
    migrant_worker = "migrant_worker"


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, index=True)

    swasthya_id: Mapped[str | None] = mapped_column(String(16), unique=True, nullable=True, index=True)
    abha_number: Mapped[str | None] = mapped_column(String(14), unique=True, nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_encrypted: Mapped[str] = mapped_column(String(1024), nullable=False)
    phone_hash: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)
    age: Mapped[int | None] = mapped_column(nullable=True)
    blood_type: Mapped[str | None] = mapped_column(String(8), nullable=True)
    allergies: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    current_medications: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    recent_diagnoses: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    language: Mapped[str] = mapped_column(String(32), default="en", nullable=False)
    state: Mapped[str | None] = mapped_column(String(64), nullable=True)

    consent_granted: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    health_records = relationship("HealthRecord", back_populates="worker", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="worker", cascade="all, delete-orphan")
    risk_profiles = relationship("RiskProfile", back_populates="worker", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="worker", cascade="all, delete-orphan")
    locations = relationship("LocationLog", back_populates="worker", cascade="all, delete-orphan")
