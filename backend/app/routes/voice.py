from fastapi import APIRouter, File, UploadFile

from app.ai_modules.bhashasehat import process_text_payload, transcribe_audio_payload
from app.schemas.voice import VoiceProcessResponse, VoiceTextRequest, VoiceTranscribeResponse

router = APIRouter(prefix="/voice", tags=["voice"])


@router.post("/transcribe", response_model=VoiceTranscribeResponse)
async def transcribe(
    file: UploadFile = File(...),
) -> VoiceTranscribeResponse:
    payload = await file.read()
    text, lang = transcribe_audio_payload(payload)
    return VoiceTranscribeResponse(text=text, detected_language=lang)


@router.post("/process", response_model=VoiceProcessResponse)
async def process_text(
    payload: VoiceTextRequest,
) -> VoiceProcessResponse:
    result = process_text_payload(
        payload.text,
        target_language=payload.target_language,
        source_language=payload.source_language,
    )
    # pyre-ignore[6]
    return VoiceProcessResponse(**result)
