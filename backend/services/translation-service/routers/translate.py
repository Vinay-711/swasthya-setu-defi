"""Translation endpoints — text and medical term translation."""

from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timezone

router = APIRouter()

# Mock translations — in production, use IndicTrans2 or Google Translate API
MOCK_TRANSLATIONS: dict[str, dict[str, str]] = {
    "hi": {
        "You have been diagnosed with silicosis.": "आपको सिलिकोसिस का निदान हुआ है।",
        "Please wear PPE at all times.": "कृपया हर समय पीपीई पहनें।",
        "Your next checkup is scheduled.": "आपकी अगली जांच निर्धारित है।",
    },
    "bn": {
        "You have been diagnosed with silicosis.": "আপনার সিলিকোসিস ধরা পড়েছে।",
        "Please wear PPE at all times.": "অনুগ্রহ করে সর্বদা পিপিই পরুন।",
    },
}


class TranslateRequest(BaseModel):
    text: str
    sourceLang: str = "en"
    targetLang: str = "hi"


class BatchTranslateRequest(BaseModel):
    texts: list[str]
    sourceLang: str = "en"
    targetLang: str = "hi"


@router.post("/text")
async def translate_text(req: TranslateRequest):
    """Translate a single text string."""
    lang_dict = MOCK_TRANSLATIONS.get(req.targetLang, {})
    translated = lang_dict.get(req.text, f"[{req.targetLang}] {req.text}")

    return {
        "original": req.text,
        "translated": translated,
        "sourceLang": req.sourceLang,
        "targetLang": req.targetLang,
        "processedAt": datetime.now(timezone.utc).isoformat(),
    }


@router.post("/batch")
async def translate_batch(req: BatchTranslateRequest):
    """Translate a batch of texts."""
    lang_dict = MOCK_TRANSLATIONS.get(req.targetLang, {})
    results = []

    for text in req.texts:
        translated = lang_dict.get(text, f"[{req.targetLang}] {text}")
        results.append({"original": text, "translated": translated})

    return {
        "results": results,
        "sourceLang": req.sourceLang,
        "targetLang": req.targetLang,
        "count": len(results),
    }


@router.get("/languages")
async def list_languages():
    """List supported languages."""
    return {
        "languages": [
            {"code": "en", "name": "English", "native": "English"},
            {"code": "hi", "name": "Hindi", "native": "हिन्दी"},
            {"code": "bn", "name": "Bengali", "native": "বাংলা"},
            {"code": "ta", "name": "Tamil", "native": "தமிழ்"},
            {"code": "te", "name": "Telugu", "native": "తెలుగు"},
            {"code": "mr", "name": "Marathi", "native": "मराठी"},
            {"code": "gu", "name": "Gujarati", "native": "ગુજરાતી"},
            {"code": "kn", "name": "Kannada", "native": "ಕನ್ನಡ"},
            {"code": "or", "name": "Odia", "native": "ଓଡ଼ିଆ"},
        ]
    }
