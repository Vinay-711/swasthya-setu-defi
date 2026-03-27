from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path


MEDICINE_PATTERN = re.compile(r"\b([A-Za-z][A-Za-z0-9\-]{2,})\s+(\d+(?:\.\d+)?\s*(?:mg|ml|mcg|g))\b", re.IGNORECASE)
DATE_PATTERN = re.compile(r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})\b")

DIAGNOSIS_KEYWORDS = [
    "silicosis",
    "byssinosis",
    "asthma",
    "tuberculosis",
    "hypertension",
    "diabetes",
    "bronchitis",
]


class DocumentAIProcessor:
    def extract_text(self, raw_bytes: bytes, filename: str) -> str:
        suffix = Path(filename).suffix.lower()

        if suffix in {".txt", ".json", ".csv"}:
            return raw_bytes.decode("utf-8", errors="ignore")

        if suffix in {".png", ".jpg", ".jpeg", ".pdf"}:
            return "MOCK_OCR_TEXT: Patient reports chronic cough and asthma. Prescribed Paracetamol 500mg and Salbutamol 100mcg."

        # Lightweight fallback when OCR stack is unavailable.
        decoded = raw_bytes.decode("utf-8", errors="ignore")
        if decoded.strip():
            return decoded

        return "Unable to decode unstructured text from binary input"

    def parse_structured(self, text: str) -> dict[str, object]:
        medicines: list[dict[str, str]] = []
        for name, dose in MEDICINE_PATTERN.findall(text):
            medicines.append({"name": name, "dosage": dose})

        diagnosis_matches = []
        lower_text = text.lower()
        for keyword in DIAGNOSIS_KEYWORDS:
            if keyword in lower_text:
                diagnosis_matches.append(keyword)

        dates = DATE_PATTERN.findall(text)

        return {
            "summary": text[:400],  # type: ignore[index]
            "medicines": medicines,
            "diagnosis": diagnosis_matches,
            "dates": dates,
            "extracted_at": datetime.utcnow().isoformat(),
        }

    def process(self, raw_bytes: bytes, filename: str) -> dict[str, object]:
        text = self.extract_text(raw_bytes=raw_bytes, filename=filename)
        structured = self.parse_structured(text)
        structured["raw_text"] = text
        return structured


processor = DocumentAIProcessor()
