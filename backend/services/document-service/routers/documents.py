"""Document management endpoints — upload, list, retrieve."""

from fastapi import APIRouter, UploadFile, File  # pyre-ignore[21]
from datetime import datetime, timezone
import uuid

router = APIRouter()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    swasthya_id: str = "unknown",
):
    """Upload a medical document (prescription, lab report, etc.)."""
    content = await file.read()
    file_size_kb = len(content) / 1024
    doc_id = str(uuid.uuid4())

    return {
        "id": doc_id,
        "swasthyaId": swasthya_id,
        "filename": file.filename,
        "contentType": file.content_type,
        "fileSizeKb": round(file_size_kb, 2),  # type: ignore
        "storagePath": f"documents/{swasthya_id}/{doc_id}",
        "status": "uploaded",
        "parsedJson": None,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/{swasthya_id}")
async def list_documents(swasthya_id: str):
    """List all documents for a worker."""
    return {
        "swasthyaId": swasthya_id,
        "documents": [
            {
                "id": "doc-demo-001",
                "filename": "prescription_march_2025.jpg",
                "contentType": "image/jpeg",
                "status": "processed",
                "parsedJson": {
                    "medicines": [{"name": "Paracetamol", "dosage": "500mg"}],
                    "diagnosis": ["Mild fever"],
                },
                "createdAt": "2025-03-15T10:30:00Z",
            },
        ],
        "totalCount": 1,
    }


@router.get("/{swasthya_id}/{doc_id}")
async def get_document(swasthya_id: str, doc_id: str):
    """Get a specific document by ID."""
    return {
        "id": doc_id,
        "swasthyaId": swasthya_id,
        "filename": "prescription.jpg",
        "status": "processed",
        "downloadUrl": f"/storage/documents/{swasthya_id}/{doc_id}",
    }


@router.delete("/{swasthya_id}/{doc_id}")
async def delete_document(swasthya_id: str, doc_id: str):
    """Delete a document."""
    return {"id": doc_id, "deleted": True}
