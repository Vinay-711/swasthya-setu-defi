from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.tracking import LocationOut, LocationUpdateRequest
from app.services.tracking_service import create_location_log, list_worker_locations
from database.session import get_db

router = APIRouter(prefix="/tracking", tags=["tracking"])


@router.post("/location", response_model=LocationOut)
async def update_location(
    payload: LocationUpdateRequest,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> LocationOut:
    row = await create_location_log(db, payload)
    return LocationOut.model_validate(row)


@router.get("/worker/{worker_id}", response_model=list[LocationOut])
async def worker_locations(
    worker_id: str,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[LocationOut]:
    rows = await list_worker_locations(db, worker_id)
    return [LocationOut.model_validate(row) for row in rows]
