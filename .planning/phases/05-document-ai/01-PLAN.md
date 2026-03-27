# Phase 5 Execution Plan: Document AI

## 1. OCR Intelligence Stub
- **File:** `app/ai_modules/document_ai.py`
- Modify `extract_text` to detect binary images (`.png`, `.jpg`, `.jpeg`, `.pdf`).
- When an image is detected, return a deterministic mock medical text containing medicines (e.g., "Paracetamol 500mg") and keywords ("asthma", "fever") to trigger the `parse_structured` logic.

## 2. Route & RBAC Updates
- **File:** `app/routes/documents.py`
- **Upload / Scan**: Update `POST /upload` and `POST /scan` to enforce `require_roles(UserRole.doctor, UserRole.asha_worker)`.
- **List / Get**: Update `GET /worker/{worker_id}` and `GET /{document_id}` to enforce list viewing rules (Doctors/Admins or the owner themselves).

## 3. Tests
- **File:** `tests/test_documents.py`
- Write comprehensive integration tests simulating:
  - Image upload by an ASHA worker acting as OCR.
  - Proper metadata extraction mapping via `parsed_json`.
  - RBAC rejection for ordinary workers trying to view others' documents.
