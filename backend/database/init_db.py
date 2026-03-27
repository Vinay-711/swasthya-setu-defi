from database.base import Base
from database.session import engine
import app.models  # noqa: F401


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
