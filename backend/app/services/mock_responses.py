# pyre-ignore-all-errors
from __future__ import annotations

import base64
import re
from datetime import datetime, timezone

from fastapi import Request
from fastapi.responses import JSONResponse, Response

from app.core.config import settings
from app.utils.qr import build_qr_png_bytes

RAMESH_WORKER_ID = "7f0f77a4-8425-4e92-a17f-7cb0f91ef001"
RAMESH_SWASTHYA_ID = "SW-100001"

HINDI_TRANSCRIPT = "mujhe seene mein dard ho raha hai aur sans lene mein takleef hai"

RAMESH_RISK_PROFILE = {
    "silicosis": 0.87,
    "byssinosis": 0.04,
    "occupational_asthma": 0.19,
    "risk_level": "HIGH",
    "predicted_disease": "silicosis",
    "top_factors": [
        {"feature": "years_in_job", "impact": 0.42, "value": "8 years"},
        {"feature": "task_stone_cutting", "impact": 0.31, "value": "daily"},
        {"feature": "ppe_usage", "impact": 0.28, "value": "rarely"},
    ],
    "recommendations": [
        "Chest X-ray immediately",
        "Spirometry test",
        "Refer to occupational health specialist",
        "Priority follow-up in 72 hours",
    ],
}

MOCK_DOCUMENT = {
    "id": "doc-mock-001",
    "worker_id": RAMESH_WORKER_ID,
    "original_path": "mock://prescriptions/ramesh-visit.png",
    "status": "processed",
    "parsed_json": {
        "summary": "OPD prescription parsed successfully",
        "medicines": [
            {"name": "Salbutamol", "dosage": "2mg"},
            {"name": "Budesonide", "dosage": "200mcg"},
            {"name": "Montelukast", "dosage": "10mg"},
        ],
        "diagnosis": ["suspected silicosis", "chronic cough"],
        "dates": ["2026-03-20"],
        "translated_text": "Suspected occupational lung disease",
    },
    "created_at": "2026-03-20T09:30:00Z",
}

MOCK_HEALTH_RECORD = {
    "id": "hr-mock-001",
    "worker_id": RAMESH_WORKER_ID,
    "record_type": "visit",
    "data_json": {
        "summary": "Persistent cough for 6 months",
        "clinic": "Surat Civil Occupational Unit",
    },
    "created_at": "2026-03-18T10:45:00Z",
    "updated_at": "2026-03-18T10:45:00Z",
}

MOCK_NOTIFICATION = {
    "id": "ntf-mock-001",
    "worker_id": RAMESH_WORKER_ID,
    "channel": "whatsapp",
    "message": "High respiratory risk detected. Visit nearest clinic.",
    "status": "sent",
    "sent_at": "2026-03-18T11:00:00Z",
    "created_at": "2026-03-18T11:00:00Z",
}

MOCK_LOCATION = {
    "id": "loc-mock-001",
    "worker_id": RAMESH_WORKER_ID,
    "state": "Gujarat",
    "city": "Surat",
    "latitude": "21.1702",
    "longitude": "72.8311",
    "source": "manual",
    "created_at": "2026-03-18T12:00:00Z",
}


def _mock_translate_text(target_language: str | None) -> str:
    target = (target_language or "").strip().lower()
    if target.startswith("en"):
        return "I have chest pain and difficulty breathing."
    if target.startswith("hi"):
        return "मुझे सीने में दर्द हो रहा है और सांस लेने में तकलीफ है।"
    if target.startswith("mr"):
        return "मला छातीत वेदना आहे आणि श्वास घेण्यास त्रास होतो आहे."
    if target.startswith("bn"):
        return "আমার বুকে ব্যথা হচ্ছে এবং শ্বাস নিতে কষ্ট হচ্ছে।"
    if target.startswith("ta"):
        return "எனக்கு மார்பில் வலி உள்ளது மற்றும் சுவாசிக்க சிரமமாக உள்ளது."
    if target.startswith("te"):
        return "నాకు ఛాతిలో నొప్పి ఉంది మరియు శ్వాస తీసుకోవడంలో ఇబ్బంది ఉంది."
    if target.startswith("kn"):
        return "ನನಗೆ ಎದೆನೋವು ಇದೆ ಮತ್ತು ಉಸಿರಾಟಕ್ಕೆ ತೊಂದರೆ ಆಗುತ್ತಿದೆ."
    if target.startswith("or") or target.startswith("od"):
        return "ମୋର ଛାତିରେ ବେଦନା ହେଉଛି ଏବଂ ଶ୍ୱାସ ନେବାରେ ଅସୁବିଧା ହେଉଛି।"
    if target.startswith("ml"):
        return "എനിക്ക് നെഞ്ചുവേദനയുണ്ട്, ശ്വസിക്കാൻ ബുദ്ധിമുട്ടുണ്ട്."
    return HINDI_TRANSCRIPT


def is_mock_mode(request: Request) -> bool:
    value = (request.query_params.get("mock") or "").strip().lower()
    return value in {"1", "true", "yes", "on"}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _token_payload() -> dict[str, object]:
    return {
        "access_token": "mock.jwt.token",
        "token_type": "bearer",
        "user": {
            "id": RAMESH_WORKER_ID,
            "email": "ramesh.worker@swasthya.in",
            "role": "worker",
            "swasthya_id": RAMESH_SWASTHYA_ID,
            "name": "Ramesh Yadav",
            "language": "hi",
            "age": 34,
            "blood_type": "O+",
            "allergies": ["dust"],
            "current_medications": ["Salbutamol inhaler"],
            "recent_diagnoses": ["chronic bronchitis"],
            "consent_granted": True,
            "created_at": "2026-03-01T09:00:00Z",
        },
    }


def _worker_record() -> dict[str, object]:
    return {
        "swasthya_id": RAMESH_SWASTHYA_ID,
        "worker": _token_payload()["user"],
        "health_records": [
            MOCK_HEALTH_RECORD,
            {
                **MOCK_HEALTH_RECORD,
                "id": "hr-mock-002",
                "record_type": "follow_up",
                "created_at": "2026-03-10T09:00:00Z",
                "updated_at": "2026-03-10T09:00:00Z",
                "data_json": {"summary": "Breathlessness while lifting heavy loads"},
            },
            {
                **MOCK_HEALTH_RECORD,
                "id": "hr-mock-003",
                "record_type": "visit",
                "created_at": "2026-03-01T08:00:00Z",
                "updated_at": "2026-03-01T08:00:00Z",
                "data_json": {"summary": "Baseline checkup after migration"},
            },
        ],
        "occupational_risk": [
            {
                "id": "risk-mock-001",
                "risk_level": "HIGH",
                "scores_json": RAMESH_RISK_PROFILE,
                "created_at": "2026-03-18T10:50:00Z",
            }
        ],
        "documents": [MOCK_DOCUMENT],
        "notifications": [MOCK_NOTIFICATION],
    }


async def build_mock_response(request: Request) -> Response:
    method = request.method.upper()
    path = request.url.path

    if not path.startswith(settings.api_prefix):
        return JSONResponse({"mock": True, "message": "Outside API prefix fallback"})

    rel = path[len(settings.api_prefix) :] or "/"

    if rel == "/health" and method == "GET":
        return JSONResponse({"status": "ok", "mode": "mock", "timestamp": _now_iso()})

    if rel in {"/auth/register", "/auth/login"} and method == "POST":
        return JSONResponse(_token_payload(), status_code=201 if rel.endswith("register") else 200)

    if rel == "/auth/me" and method == "GET":
        return JSONResponse(_token_payload()["user"])

    if rel == "/identity/create" and method == "POST":
        qr_content = f"/worker/{RAMESH_SWASTHYA_ID}".encode()
        qr_data_url = f"data:image/png;base64,{base64.b64encode(qr_content).decode()}"
        return JSONResponse(
            {
                "swasthya_id": RAMESH_SWASTHYA_ID,
                "worker_id": RAMESH_WORKER_ID,
                "qr_data_url": qr_data_url,
            }
        )

    if re.fullmatch(r"/identity/[^/]+/qr", rel) and method == "GET":
        return Response(content=build_qr_png_bytes(f"/worker/{RAMESH_SWASTHYA_ID}"), media_type="image/png")

    if re.fullmatch(r"/identity/[^/]+/consent", rel) and method == "PUT":
        swasthya_id = rel.split("/")[2]
        return JSONResponse({"swasthya_id": swasthya_id, "consent_granted": True})

    if re.fullmatch(r"/identity/[^/]+/record", rel) and method == "GET":
        return JSONResponse(_worker_record())

    if rel == "/health-records/" and method == "POST":
        return JSONResponse(MOCK_HEALTH_RECORD, status_code=201)

    if re.fullmatch(r"/health-records/worker/[^/]+", rel) and method == "GET":
        return JSONResponse([MOCK_HEALTH_RECORD])

    if re.fullmatch(r"/health-records/[^/]+", rel) and method == "PUT":
        return JSONResponse(MOCK_HEALTH_RECORD)

    if re.fullmatch(r"/health-records/[^/]+", rel) and method == "DELETE":
        return Response(status_code=204)

    if rel in {"/documents/upload", "/documents/scan"} and method == "POST":
        return JSONResponse(MOCK_DOCUMENT, status_code=201)

    if re.fullmatch(r"/documents/worker/[^/]+", rel) and method == "GET":
        return JSONResponse([MOCK_DOCUMENT])

    if re.fullmatch(r"/documents/[^/]+/translate", rel) and method == "POST":
        return JSONResponse(MOCK_DOCUMENT)

    if re.fullmatch(r"/documents/[^/]+", rel) and method == "GET":
        return JSONResponse(MOCK_DOCUMENT)

    if rel == "/occupational/risk-profile" and method in {"GET", "POST"}:
        return JSONResponse(RAMESH_RISK_PROFILE)

    if re.fullmatch(r"/occupational/recommendations/[^/]+", rel) and method == "GET":
        return JSONResponse(
            {
                "worker_id": RAMESH_WORKER_ID,
                "risk_level": "HIGH",
                "predicted_disease": "silicosis",
                "recommendations": RAMESH_RISK_PROFILE["recommendations"],
            }
        )

    if re.fullmatch(r"/occupational/explain/[^/]+", rel) and method == "GET":
        return JSONResponse(
            {
                "risk_id": "risk-mock-001",
                "risk_level": "HIGH",
                "top_factors": RAMESH_RISK_PROFILE["top_factors"],
                "scores": {
                    "silicosis": RAMESH_RISK_PROFILE["silicosis"],
                    "byssinosis": RAMESH_RISK_PROFILE["byssinosis"],
                    "occupational_asthma": RAMESH_RISK_PROFILE["occupational_asthma"],
                },
            }
        )

    if re.fullmatch(r"/occupational/history/[^/]+", rel) and method == "GET":
        return JSONResponse(
            [
                {
                    "id": "risk-mock-001",
                    "occupation": "stone_quarry",
                    "risk_level": "HIGH",
                    "scores_json": RAMESH_RISK_PROFILE,
                    "created_at": "2026-03-18T10:50:00Z",
                }
            ]
        )

    if rel == "/voice/transcribe" and method == "POST":
        return JSONResponse({"text": HINDI_TRANSCRIPT, "detected_language": "hi"})

    if rel in {"/voice/process", "/voice/translate"} and method == "POST":
        target_language = "en"
        input_text = HINDI_TRANSCRIPT
        try:
            body = await request.json()
            if isinstance(body, dict):
                input_text = str(body.get("text") or HINDI_TRANSCRIPT)
                target_language = str(
                    body.get("target_language")
                    or body.get("to_lang")
                    or body.get("targetLang")
                    or "en"
                )
        except Exception:
            pass
        return JSONResponse(
            {
                "text": input_text,
                "detected_language": "hi",
                "translated_text": _mock_translate_text(target_language),
                "tts_audio_base64": base64.b64encode(b"mock-tts-audio").decode(),
            }
        )

    if rel == "/ai/chat" and method == "POST":
        message = "I can help with risk analysis, QR scan, OCR documents, and voice flow."
        language = "en"
        try:
            body = await request.json()
            if isinstance(body, dict):
                message = str(body.get("message") or message)
                language = str(body.get("language") or language).lower()
        except Exception:
            pass

        lower = message.lower()
        reply = "I can help with risk analysis, QR scan, OCR documents, and voice flow."
        if "risk" in lower:
            reply = "Open Risk Analysis, fill worker profile, and click Analyze Occupational Risk."
        elif "voice" in lower or "audio" in lower:
            reply = "Use Voice-first Intake in Risk Analysis and pick source/target language."
        elif "qr" in lower or "scan" in lower:
            reply = "Open Scan QR page and enter SW-100001 to fetch clinic history."
        elif "document" in lower or "ocr" in lower:
            reply = "Open Upload Documents and click Digitize with OCR."

        if language.startswith("hi"):
            reply = "जोखिम, QR स्कैन, OCR दस्तावेज़ और वॉइस फ्लो में मैं आपकी मदद कर सकता हूँ।"

        return JSONResponse(
            {
                "reply": reply,
                "model": "mock-gemini",
                "used_fallback": True,
            }
        )

    if rel == "/notifications/trigger" and method == "POST":
        return JSONResponse(MOCK_NOTIFICATION)

    if re.fullmatch(r"/notifications/worker/[^/]+", rel) and method == "GET":
        return JSONResponse([MOCK_NOTIFICATION])

    if rel == "/tracking/location" and method == "POST":
        return JSONResponse(MOCK_LOCATION)

    if re.fullmatch(r"/tracking/worker/[^/]+", rel) and method == "GET":
        return JSONResponse([MOCK_LOCATION])

    # ── KaamSuraksha endpoints ──

    if rel in {"/kaamsuraksha/score"} and method == "POST":
        return JSONResponse(RAMESH_RISK_PROFILE)

    if rel == "/kaamsuraksha/score/batch" and method == "POST":
        return JSONResponse({
            "total": 15,
            "results": [
                {"worker_id": "ramesh", "risk_level": "HIGH", "risk_score": 0.81,
                 "predicted_disease": "silicosis", "occupation": "construction_mason"},
                {"worker_id": "dinesh", "risk_level": "HIGH", "risk_score": 0.91,
                 "predicted_disease": "silicosis", "occupation": "stone_quarry"},
                {"worker_id": "shankar", "risk_level": "HIGH", "risk_score": 0.82,
                 "predicted_disease": "occupational_asthma", "occupation": "stone_quarry"},
                {"worker_id": "parvati", "risk_level": "HIGH", "risk_score": 0.81,
                 "predicted_disease": "byssinosis", "occupation": "textile_mill"},
                {"worker_id": "gopal", "risk_level": "HIGH", "risk_score": 0.88,
                 "predicted_disease": "cwp", "occupation": "coal_mining"},
                {"worker_id": "mohan", "risk_level": "HIGH", "risk_score": 0.82,
                 "predicted_disease": "chemical_dermatitis", "occupation": "chemical_factory"},
                {"worker_id": "kamla", "risk_level": "HIGH", "risk_score": 0.72,
                 "predicted_disease": "copd", "occupation": "textile_mill"},
                {"worker_id": "suresh", "risk_level": "MEDIUM", "risk_score": 0.74,
                 "predicted_disease": "occupational_asthma", "occupation": "construction_rebar"},
                {"worker_id": "raju", "risk_level": "MEDIUM", "risk_score": 0.78,
                 "predicted_disease": "musculoskeletal", "occupation": "scaffolding"},
                {"worker_id": "bharat", "risk_level": "MEDIUM", "risk_score": 0.78,
                 "predicted_disease": "nihl", "occupation": "mining"},
                {"worker_id": "lakshman", "risk_level": "MEDIUM", "risk_score": 0.75,
                 "predicted_disease": "heat_stroke", "occupation": "brick_kiln"},
                {"worker_id": "meena", "risk_level": "MEDIUM", "risk_score": 0.62,
                 "predicted_disease": "nutritional_risk", "occupation": "domestic_worker"},
                {"worker_id": "sunita", "risk_level": "MEDIUM", "risk_score": 0.72,
                 "predicted_disease": "pesticide_poisoning", "occupation": "agriculture"},
                {"worker_id": "savitri", "risk_level": "MEDIUM", "risk_score": 0.82,
                 "predicted_disease": "nutritional_risk", "occupation": "domestic_worker"},
                {"worker_id": "geeta", "risk_level": "LOW", "risk_score": 0.68,
                 "predicted_disease": "gastric_risk", "occupation": "agriculture"},
            ],
            "summary": {"LOW": 1, "MEDIUM": 7, "HIGH": 7},
        })

    if re.fullmatch(r"/kaamsuraksha/score/[^/]+", rel) and method == "GET":
        return JSONResponse(RAMESH_RISK_PROFILE)

    if re.fullmatch(r"/kaamsuraksha/employer/dashboard/[^/]+", rel) and method == "GET":
        return JSONResponse({
            "employer_name": "Bengaluru BuildCon Pvt Ltd",
            "total_workers": 250,
            "registered_workers": 15,
            "health_status": {"healthy": 168, "at_risk": 56, "critical": 26},
            "compliance": {"percentage": 93.2, "ppe": 96.0, "screenings": 88.0, "training": 95.5},
            "top_risk_occupations": [
                {"rank": 1, "name": "Stone Quarry / Cutting", "workers": 3, "risk_score": 9.1,
                 "detail": "Silicosis (91%), occupational asthma (82%)"},
                {"rank": 2, "name": "Coal / Underground Mining", "workers": 2, "risk_score": 8.8,
                 "detail": "CWP (88%), chronic bronchitis (82%)"},
                {"rank": 3, "name": "Chemical Factory", "workers": 1, "risk_score": 8.2,
                 "detail": "Chemical dermatitis (82%), respiratory (71%)"},
                {"rank": 4, "name": "Textile Mill", "workers": 2, "risk_score": 8.1,
                 "detail": "Byssinosis (81%), COPD (65%)"},
                {"rank": 5, "name": "Brick Kiln", "workers": 1, "risk_score": 7.5,
                 "detail": "Heat stroke (75%), musculoskeletal (72%)"},
                {"rank": 6, "name": "Construction (Rebar/Scaffold)", "workers": 2, "risk_score": 7.4,
                 "detail": "Fall risk (72%), respiratory (74%)"},
                {"rank": 7, "name": "Agriculture", "workers": 2, "risk_score": 7.0,
                 "detail": "Pesticide poisoning (72%), musculoskeletal (55%)"},
                {"rank": 8, "name": "Domestic Work", "workers": 2, "risk_score": 6.0,
                 "detail": "Nutritional risk (82%), anemia (58%)"},
            ],
        })

    if rel == "/kaamsuraksha/occupations/risk-ranking" and method == "GET":
        return JSONResponse([
            {"rank": 1, "name": "Sandblasting", "workers": 0, "risk_score": 9.1,
             "detail": "Acute silicosis, lung fibrosis"},
            {"rank": 2, "name": "Stone Cutting", "workers": 0, "risk_score": 8.7,
             "detail": "Silicosis, respiratory exposure"},
            {"rank": 3, "name": "Mining", "workers": 0, "risk_score": 8.2,
             "detail": "Silicosis, tunnel collapse"},
            {"rank": 4, "name": "Chemical Handling", "workers": 0, "risk_score": 7.5,
             "detail": "Toxic fumes, skin burns"},
            {"rank": 5, "name": "Welding & Metal Work", "workers": 0, "risk_score": 7.2,
             "detail": "Fume inhalation, burn risk"},
        ])

    return JSONResponse(
        {
            "mock": True,
            "message": "Demo-safe fallback response.",
            "path": path,
            "method": method,
            "timestamp": _now_iso(),
        }
    )
