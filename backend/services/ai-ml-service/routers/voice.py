"""Voice-to-text processing using Whisper (mock for demo)."""

from fastapi import APIRouter, UploadFile, File
from datetime import datetime, timezone

router = APIRouter()


@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """Transcribe audio file to text using Whisper model."""
    content = await file.read()
    file_size_kb = len(content) / 1024

    # Mock transcription — in production, run Whisper inference
    return {
        "filename": file.filename,
        "fileSizeKb": round(file_size_kb, 2),
        "language": "hi",
        "transcript": "मुझे सांस लेने में तकलीफ हो रही है और खांसी भी आ रही है।",
        "translatedText": "I am having difficulty breathing and also have a cough.",
        "confidence": 0.92,
        "durationMs": 3200,
        "processedAt": datetime.now(timezone.utc).isoformat(),
    }


@router.post("/symptom-extract")
async def extract_symptoms(file: UploadFile = File(...)):
    """Extract symptoms from voice recording."""
    await file.read()

    return {
        "symptoms": [
            {"name": "breathlessness", "confidence": 0.94, "severity": "moderate"},
            {"name": "persistent_cough", "confidence": 0.88, "severity": "mild"},
        ],
        "recommendedAction": "Schedule spirometry test",
        "urgency": "medium",
    }
