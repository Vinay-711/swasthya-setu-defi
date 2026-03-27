import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.core.config import settings

async def drop_all():
    engine = create_async_engine(settings.database_url)
    async with engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA public CASCADE"))
        await conn.execute(text("CREATE SCHEMA public"))
    print("Dropped and recreated public schema.")

if __name__ == "__main__":
    asyncio.run(drop_all())
