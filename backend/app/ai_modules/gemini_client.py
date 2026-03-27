from __future__ import annotations

import json
from datetime import datetime, timezone
from threading import Lock
import urllib.error
import urllib.request

from app.core.config import settings

FREE_TIER_MODEL_ALLOWLIST = {
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
}

_cap_lock = Lock()
_cap_day = ""
_cap_count = 0


def _resolve_model() -> str:
    requested = settings.gemini_model.strip()
    free_default = settings.gemini_free_tier_model.strip() or "gemini-2.5-flash-lite"

    if settings.gemini_free_tier_only:
        if requested and requested in FREE_TIER_MODEL_ALLOWLIST:
            return requested
        if free_default in FREE_TIER_MODEL_ALLOWLIST:
            return free_default
        return "gemini-2.5-flash-lite"

    return requested or free_default


def resolved_gemini_model() -> str:
    return _resolve_model()


def _allow_request_under_cap() -> bool:
    daily_cap = int(settings.gemini_daily_request_cap)
    if daily_cap <= 0:
        return True

    now_day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    global _cap_day, _cap_count
    with _cap_lock:
        if _cap_day != now_day:
            _cap_day = now_day
            _cap_count = 0
        if _cap_count >= daily_cap:
            return False
        _cap_count += 1
    return True


def gemini_generate_text(
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = 0.2,
    max_output_tokens: int = 512,
) -> str | None:
    api_key = settings.gemini_api_key.strip()
    if not api_key:
        return None

    if not _allow_request_under_cap():
        return None

    model = _resolve_model()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    payload: dict[str, object] = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_output_tokens,
        },
    }

    if system_instruction:
        payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

    request = urllib.request.Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            raw = response.read().decode("utf-8")
        decoded = json.loads(raw)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None

    candidates = decoded.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        return None

    candidate = candidates[0]
    content = candidate.get("content")
    if not isinstance(content, dict):
        return None

    parts = content.get("parts")
    if not isinstance(parts, list):
        return None

    chunks: list[str] = []
    for part in parts:
        if isinstance(part, dict):
            text = part.get("text")
            if isinstance(text, str) and text.strip():
                chunks.append(text.strip())

    if not chunks:
        return None

    return "\n".join(chunks).strip()
