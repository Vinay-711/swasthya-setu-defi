from pydantic import BaseModel


class VoiceTextRequest(BaseModel):
    text: str
    source_language: str | None = None
    target_language: str | None = None


class VoiceTranscribeResponse(BaseModel):
    text: str
    detected_language: str


class VoiceProcessResponse(BaseModel):
    text: str
    detected_language: str
    translated_text: str
    tts_audio_base64: str
