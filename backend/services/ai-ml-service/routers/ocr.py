"""OCR / Document AI using LayoutLMv3 (mock for demo)."""

from fastapi import APIRouter, UploadFile, File
from datetime import datetime, timezone

router = APIRouter()


@router.post("/extract")
async def extract_document(file: UploadFile = File(...)):
    """Extract structured data from a medical document image."""
    content = await file.read()
    file_size_kb = len(content) / 1024

    return {
        "filename": file.filename,
        "fileSizeKb": round(file_size_kb, 2),
        "documentType": "prescription",
        "extracted": {
            "patientName": "Demo Worker",
            "doctorName": "Dr. Sharma",
            "date": "2025-03-15",
            "medicines": [
                {"name": "Paracetamol", "dosage": "500mg", "frequency": "3x daily"},
                {"name": "Salbutamol", "dosage": "100mcg", "frequency": "as needed"},
            ],
            "diagnosis": ["Occupational asthma", "Mild bronchitis"],
            "followUp": "2025-04-15",
        },
        "confidence": 0.91,
        "modelVersion": "layoutlmv3-v1.2",
        "processedAt": datetime.now(timezone.utc).isoformat(),
    }
