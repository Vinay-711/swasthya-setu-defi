from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[3]
BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "SwasthyaSetu"
    api_prefix: str = "/api/v1"
    environment: str = "development"

    secret_key: str = "change-me-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    encryption_key: str = ""

    database_url: str = "postgresql+asyncpg://swasthya:swasthya@localhost:5432/swasthyasetu"
    mongodb_url: str = "mongodb://localhost:27017/swasthyasetu"
    redis_url: str = "redis://localhost:6379/0"
    storage_dir: str = "backend/storage"

    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    log_level: str = "INFO"

    qr_record_path_prefix: str = "/worker"

    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    gemini_free_tier_only: bool = True
    gemini_free_tier_model: str = "gemini-2.5-flash-lite"
    gemini_daily_request_cap: int = 250
    allow_start_without_db: bool = True

    model_config = SettingsConfigDict(
        env_file=[
            str(ROOT_DIR / ".env"),
            str(BACKEND_DIR / ".env"),
            ".env",
        ],
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # pyre-ignore[56]
    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> Any:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
