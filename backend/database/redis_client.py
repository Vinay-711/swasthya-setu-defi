from app.core.config import settings

try:
    import redis.asyncio as redis
except Exception:  # pragma: no cover
    redis = None  # type: ignore

redis_client = redis.from_url(settings.redis_url, decode_responses=True) if redis else None
