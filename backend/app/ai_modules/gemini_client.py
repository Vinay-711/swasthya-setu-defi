from __future__ import annotations

import json
import urllib.error
import urllib.request

from app.core.config import settings


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

    model = settings.gemini_model.strip() or "gemini-1.5-flash"
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
