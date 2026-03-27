# Phase 5: Document AI Context

## Objective
Digitize paper records automatically to fulfill requirement CLIN-03.

## Requirements
- **CLIN-03**: System can extract structured text from uploaded prescription images using OCR.

## Baseline
A foundational `Document` model and API routes exist (e.g., `POST /documents/upload` and `app/ai_modules/document_ai.py`). However:
1. The OCR processor (`DocumentAIProcessor`) currently crashes or rejects binary image files (it tries to decode as UTF-8).
2. The routes lack appropriate RBAC, allowing anyone to upload or view documents.

For MVP purposes, the "OCR" logic will return a structured mock text string for `.png`, `.jpg`, and `.jpeg` extensions, which the structured parser will then successfully extract medicines and diagnoses from.
