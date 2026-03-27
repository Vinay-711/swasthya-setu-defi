from fastapi import APIRouter

from app.ai_modules.bhashasehat import normalize_language_code
from app.ai_modules.gemini_client import gemini_generate_text, resolved_gemini_model
from app.schemas.ai import AIChatRequest, AIChatResponse

router = APIRouter(prefix="/ai", tags=["ai"])


def _fallback_reply(message: str) -> str:
    query = message.lower()
    if "silicosis" in query:
        return (
            "Silicosis is a lung disease caused by long-term inhalation of silica dust. "
            "Use N95/PPE, reduce dust exposure, and do regular chest X-ray and spirometry screening."
        )
    if "byssinosis" in query:
        return (
            "Byssinosis is a lung condition linked to cotton/textile dust exposure. "
            "Reduce dust, use masks, and schedule pulmonary function testing."
        )
    if "risk" in query:
        return "Open Risk Analysis, enter worker profile, then click Analyze Occupational Risk."
    if "voice" in query or "audio" in query:
        return "Use Voice-first Intake in the left panel and choose source/target language."
    if "qr" in query or "scan" in query:
        return "Go to Scan QR page and enter Worker ID like SW-100001 to load clinic history."
    if "document" in query or "ocr" in query:
        return "Open Upload Documents and click Digitize with OCR for structured extraction."
    if "hindi" in query or "language" in query or "multilingual" in query:
        return "Click Language toggle and use Voice-first translation for multilingual support."
    return "I can help with risk analysis, QR scan, OCR documents, and multilingual voice flow."


@router.post("/chat", response_model=AIChatResponse)
async def chat(payload: AIChatRequest) -> AIChatResponse:
    target_lang = normalize_language_code(payload.language) or "en"
    lang_hint = "Hindi" if target_lang == "hi" else "English"
    active_model = resolved_gemini_model()
    prompt = (
        "You are Swasthya AI assistant for migrant worker healthcare.\n"
        "Keep response short, practical, and demo-focused.\n"
        f"Respond in {lang_hint}.\n"
        f"User: {payload.message}"
    )
    reply = gemini_generate_text(
        prompt,
        system_instruction=(
            "You are Swasthya AI. Give concise actionable guidance for the app workflow."
        ),
        temperature=0.2,
        max_output_tokens=220,
    )

    if not reply:
        return AIChatResponse(
            reply=_fallback_reply(payload.message),
            model=f"{active_model}(fallback)",
            used_fallback=True,
        )

    return AIChatResponse(reply=reply, model=active_model, used_fallback=False)
