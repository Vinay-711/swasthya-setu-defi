from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.schemas.identity import ConsentUpdateRequest, IdentityCreateRequest, IdentityCreateResponse, WorkerRecordResponse, LinkABHARequest
from app.services.identity_service import build_worker_record, create_identity, get_worker_by_swasthya_id, set_worker_consent, link_worker_abha
from app.utils.qr import build_qr_png_bytes
from database.session import get_db

router = APIRouter(prefix="/identity", tags=["identity"])


@router.post("/create", response_model=IdentityCreateResponse)
async def create_worker_identity(
    payload: IdentityCreateRequest,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.migrant_worker, UserRole.admin, UserRole.doctor)),
) -> IdentityCreateResponse:
    try:
        worker, qr_data_url = await create_identity(db, payload.user_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return IdentityCreateResponse(
        swasthya_id=worker.swasthya_id or "",
        worker_id=worker.id,
        qr_data_url=qr_data_url,
    )


@router.get("/{swasthya_id}/qr")
async def get_qr_png(
    swasthya_id: str,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Response:
    worker = await get_worker_by_swasthya_id(db, swasthya_id)
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker not found")

    png_bytes = build_qr_png_bytes(f"/worker/{swasthya_id}")
    return Response(content=png_bytes, media_type="image/png")


@router.put("/{swasthya_id}/consent")
async def update_consent(
    swasthya_id: str,
    payload: ConsentUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, object]:
    worker = await get_worker_by_swasthya_id(db, swasthya_id)
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker not found")

    if current_user.id != worker.id and current_user.role not in {UserRole.admin, UserRole.doctor}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot update consent for this worker")

    updated = await set_worker_consent(db, swasthya_id=swasthya_id, consent_granted=payload.consent_granted)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker not found")

    return {"swasthya_id": swasthya_id, "consent_granted": updated.consent_granted}


@router.post("/{swasthya_id}/link-abha")
async def link_abha(
    swasthya_id: str,
    payload: LinkABHARequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, str | None]:
    worker = await get_worker_by_swasthya_id(db, swasthya_id)
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker not found")

    if current_user.id != worker.id and current_user.role not in {UserRole.admin, UserRole.doctor}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot link ABHA for this worker")

    updated = await link_worker_abha(db, swasthya_id=swasthya_id, abha_number=payload.abha_number)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker not found")

    return {"swasthya_id": swasthya_id, "abha_number": updated.abha_number}


@router.get("/{swasthya_id}/record", response_model=WorkerRecordResponse)
async def get_worker_record(
    swasthya_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> WorkerRecordResponse:
    record = await build_worker_record(db, swasthya_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker record not found")

    if not record.worker.consent_granted and current_user.id != record.worker.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Consent not granted by worker")

    return record
