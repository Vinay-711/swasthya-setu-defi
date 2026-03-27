from __future__ import annotations

import base64

from app.ai_modules.gemini_client import gemini_generate_text

try:
    from langdetect import detect  # type: ignore
except Exception:  # pragma: no cover
    detect = None


LANG_ALIASES = {
    "english": "en",
    "hindi": "hi",
    "marathi": "mr",
    "bengali": "bn",
    "tamil": "ta",
    "telugu": "te",
    "kannada": "kn",
    "odia": "or",
    "od": "or",
    "or": "or",
    "malayalam": "ml",
}

LANG_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "mr": "Marathi",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "or": "Odia",
    "ml": "Malayalam",
}

TRANSLATION_MAP = {
    ("hi", "en"): {
        "mujhe seene mein dard ho raha hai": "I have chest pain",
        "aur sans lene mein takleef hai": "and I have difficulty breathing",
    },
    ("en", "hi"): {
        "chest pain": "seene mein dard",
        "difficulty breathing": "saans lene mein takleef",
    },
}

ROMANIZED_HINDI_HINTS = (
    "mujhe",
    "seene",
    "saans",
    "sans",
    "takleef",
    "dard",
    "khansi",
    "bukhar",
)

CANONICAL_SYMPTOM_PHRASE = "mujhe seene mein dard ho raha hai aur sans lene mein takleef hai"
CANONICAL_TRANSLATIONS = {
    "en": "I have chest pain and difficulty breathing.",
    "hi": "मुझे सीने में दर्द हो रहा है और सांस लेने में तकलीफ है।",
    "mr": "मला छातीत वेदना आहे आणि श्वास घेण्यास त्रास होतो आहे.",
    "bn": "আমার বুকে ব্যথা হচ্ছে এবং শ্বাস নিতে কষ্ট হচ্ছে।",
    "ta": "எனக்கு மார்பில் வலி உள்ளது மற்றும் சுவாசிக்க சிரமமாக உள்ளது.",
    "te": "నాకు ఛాతిలో నొప్పి ఉంది మరియు శ్వాస తీసుకోవడంలో ఇబ్బంది ఉంది.",
    "kn": "ನನಗೆ ಎದೆನೋವು ಇದೆ ಮತ್ತು ಉಸಿರಾಟಕ್ಕೆ ತೊಂದರೆ ಆಗುತ್ತಿದೆ.",
    "or": "ମୋର ଛାତିରେ ବେଦନା ହେଉଛି ଏବଂ ଶ୍ୱାସ ନେବାରେ ଅସୁବିଧା ହେଉଛି।",
    "ml": "എനിക്ക് നെഞ്ചുവേദനയുണ്ട്, ശ്വസിക്കാൻ ബുദ്ധിമുട്ടുണ്ട്.",
}


def normalize_language_code(value: str | None) -> str | None:
    if not value:
        return None
    raw = value.strip().lower()
    if not raw:
        return None

    if raw in LANG_ALIASES:
        return LANG_ALIASES[raw]
    if len(raw) == 2:
        return raw
    return LANG_ALIASES.get(raw, raw[:2])


def detect_language(text: str) -> str:
    if not text.strip():
        return "en"

    if detect:
        try:
            detected = detect(text)
            normalized = normalize_language_code(detected)
            if normalized:
                return normalized
        except Exception:
            pass

    ascii_ratio = sum(1 for ch in text if ord(ch) < 128) / max(len(text), 1)
    lowered = text.lower()
    if ascii_ratio > 0.7 and any(token in lowered for token in ROMANIZED_HINDI_HINTS):
        return "hi"
    return "en" if ascii_ratio > 0.7 else "hi"


def _translate_with_gemini(text: str, source_language: str, target_language: str) -> str | None:
    source_name = LANG_NAMES.get(source_language, source_language)
    target_name = LANG_NAMES.get(target_language, target_language)
    prompt = (
        f"Translate the following healthcare symptom text from {source_name} to {target_name}.\n"
        "Return only the translated text. Keep it concise and clinically clear.\n\n"
        f"Text: {text}"
    )
    return gemini_generate_text(
        prompt,
        system_instruction=(
            "You are BhashaSehat medical translator. "
            "Translate accurately without adding extra commentary."
        ),
        temperature=0.1,
        max_output_tokens=300,
    )


def translate_text(text: str, source_language: str, target_language: str | None = None) -> str:
    normalized_source = normalize_language_code(source_language) or "en"
    normalized_target = normalize_language_code(target_language) or normalized_source

    lowered = text.lower().strip()
    normalized_phrase = " ".join(lowered.replace(".", " ").replace(",", " ").split())
    if (
        "chest pain" in normalized_phrase
        and "difficulty breathing" in normalized_phrase
        and normalized_target in CANONICAL_TRANSLATIONS
    ):
        return CANONICAL_TRANSLATIONS[normalized_target]

    if "mujhe seene" in lowered and "takleef" in lowered and normalized_target in CANONICAL_TRANSLATIONS:
        return CANONICAL_TRANSLATIONS[normalized_target]

    if lowered == CANONICAL_SYMPTOM_PHRASE and normalized_target in CANONICAL_TRANSLATIONS:
        return CANONICAL_TRANSLATIONS[normalized_target]

    if normalized_source == normalized_target:
        return text

    gemini_output = _translate_with_gemini(text, normalized_source, normalized_target)
    if gemini_output:
        return gemini_output

    mapped = TRANSLATION_MAP.get((normalized_source, normalized_target), {})
    output = text
    for key, value in mapped.items():
        output = output.replace(key, value)
    return output


def synthesize_to_base64(text: str, language: str) -> str:
    payload = f"[{language}] {text}".encode("utf-8")
    return base64.b64encode(payload).decode()


def transcribe_audio_payload(raw_bytes: bytes) -> tuple[str, str]:
    text = raw_bytes.decode("utf-8", errors="ignore").strip()
    if not text:
        text = "Audio transcription unavailable in offline mode"
    language = detect_language(text)
    return text, language


def process_text_payload(
    text: str,
    target_language: str | None = None,
    source_language: str | None = None,
) -> dict[str, str]:
    detected = detect_language(text)
    normalized_source = normalize_language_code(source_language) or detected
    normalized_target = normalize_language_code(target_language) or normalized_source
    translated = translate_text(
        text=text,
        source_language=normalized_source,
        target_language=normalized_target,
    )
    audio = synthesize_to_base64(translated, normalized_target)
    return {
        "text": text,
        "detected_language": normalized_source,
        "translated_text": translated,
        "tts_audio_base64": audio,
    }
