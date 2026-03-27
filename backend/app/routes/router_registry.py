# pyre-unsafe
from fastapi import APIRouter

from app.routes import (
    ai_router,
    auth_router,
    documents_router,
    health_records_router,
    health_router,
    identity_router,
    kaamsuraksha_router,
    notifications_router,
    occupational_router,
    tracking_router,
    voice_router,
)

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(ai_router)
api_router.include_router(identity_router)
api_router.include_router(health_records_router)
api_router.include_router(documents_router)
api_router.include_router(occupational_router)
api_router.include_router(kaamsuraksha_router)
api_router.include_router(notifications_router)
api_router.include_router(tracking_router)
api_router.include_router(voice_router)
