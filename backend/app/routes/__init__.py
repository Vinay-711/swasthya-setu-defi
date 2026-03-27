# pyre-unsafe
from app.routes.auth import router as auth_router
from app.routes.ai import router as ai_router
from app.routes.documents import router as documents_router
from app.routes.health import router as health_router
from app.routes.health_records import router as health_records_router
from app.routes.identity import router as identity_router
from app.routes.kaamsuraksha import router as kaamsuraksha_router
from app.routes.notifications import router as notifications_router
from app.routes.occupational import router as occupational_router
from app.routes.tracking import router as tracking_router
from app.routes.voice import router as voice_router

__all__ = [
    "auth_router",
    "ai_router",
    "documents_router",
    "health_router",
    "health_records_router",
    "identity_router",
    "kaamsuraksha_router",
    "notifications_router",
    "occupational_router",
    "tracking_router",
    "voice_router",
]
