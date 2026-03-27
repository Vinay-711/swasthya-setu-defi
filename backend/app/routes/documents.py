from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.schemas.documents import DocumentOut, DocumentTranslateRequest
from app.services.document_service import document_service
from database.session import get_db

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
async def upload_document(
    worker_id: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.doctor, UserRole.asha_worker)),
) -> DocumentOut:
    payload = await file.read()
    if not payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file is empty")

    row = await document_service.create_document(
        db=db,
        worker_id=worker_id,
        file_name=file.filename or "document.bin",
        file_bytes=payload,
    )
    return DocumentOut.model_validate(row)


@router.post("/scan", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
async def scan_document(
    worker_id: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.doctor, UserRole.asha_worker)),
) -> DocumentOut:
    payload = await file.read()
    if not payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file is empty")

    row = await document_service.create_document(
        db=db,
        worker_id=worker_id,
        file_name=file.filename or "scan.bin",
        file_bytes=payload,
    )
    return DocumentOut.model_validate(row)


@router.get("/worker/{worker_id}", response_model=list[DocumentOut])
async def list_worker_documents(
    worker_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[DocumentOut]:
    if current_user.role not in [UserRole.admin, UserRole.doctor] and current_user.id != worker_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view these documents")
        
    rows = await document_service.list_documents_by_worker(db, worker_id)
    return [DocumentOut.model_validate(row) for row in rows]


@router.get("/{document_id}", response_model=DocumentOut)
async def get_document(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DocumentOut:
    row = await document_service.get_document(db, document_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        
    if current_user.role not in [UserRole.admin, UserRole.doctor] and current_user.id != row.worker_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this document")
        
    return DocumentOut.model_validate(row)


@router.post("/{document_id}/translate", response_model=DocumentOut)
async def translate_document(
    document_id: str,
    payload: DocumentTranslateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DocumentOut:
    row = await document_service.get_document(db, document_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        
    if current_user.role not in [UserRole.admin, UserRole.doctor] and current_user.id != row.worker_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this document")

    row = await document_service.translate_document(db, row, payload.target_language)
    return DocumentOut.model_validate(row)
