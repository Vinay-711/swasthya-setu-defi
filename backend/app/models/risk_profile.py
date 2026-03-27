from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class RiskProfile(Base):
    __tablename__ = "risk_profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    worker_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    occupation: Mapped[str] = mapped_column(String(128), nullable=False)
    tasks_json: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    symptoms_json: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    years_in_job: Mapped[int] = mapped_column(nullable=False)
    scores_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    worker = relationship("User", back_populates="risk_profiles")
