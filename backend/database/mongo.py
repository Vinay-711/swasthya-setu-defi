from app.core.config import settings

try:
    from motor.motor_asyncio import AsyncIOMotorClient
except Exception:  # pragma: no cover
    AsyncIOMotorClient = None  # type: ignore

mongo_client = None
mongo_db = None

if AsyncIOMotorClient is not None:
    mongo_client = AsyncIOMotorClient(settings.mongodb_url)
    mongo_db = mongo_client.get_default_database()
