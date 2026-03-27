from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.schemas.health_records import (
    HealthRecordCreate,
    HealthRecordListResponse,
    HealthRecordOut,
    HealthRecordUpdate,
)
from app.services.health_record_service import (
    create_health_record,
    delete_health_record,
    get_health_record,
    list_worker_health_records,
    update_health_record,
)
from database.session import get_db

router = APIRouter(prefix="/health-records", tags=["health-records"])


@router.post("/", response_model=HealthRecordOut, status_code=status.HTTP_201_CREATED)
async def create_record(
    payload: HealthRecordCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.doctor, UserRole.asha_worker)),
) -> HealthRecordOut:
    row = await create_health_record(db, payload)
    return HealthRecordOut.model_validate(row)


@router.get("/worker/{worker_id}", response_model=HealthRecordListResponse)
async def list_records(
    worker_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> HealthRecordListResponse:
    if current_user.role not in [UserRole.doctor, UserRole.admin] and current_user.id != worker_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these records",
        )
    rows, total = await list_worker_health_records(db, worker_id, skip=skip, limit=limit)
    return HealthRecordListResponse(
        items=[HealthRecordOut.model_validate(row) for row in rows],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.put("/{record_id}", response_model=HealthRecordOut)
async def update_record(
    record_id: str,
    payload: HealthRecordUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> HealthRecordOut:
    row = await get_health_record(db, record_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Health record not found")
    updated = await update_health_record(db, row, payload)
    return HealthRecordOut.model_validate(updated)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_record(
    record_id: str,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Response:
    row = await get_health_record(db, record_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Health record not found")
    await delete_health_record(db, row)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
