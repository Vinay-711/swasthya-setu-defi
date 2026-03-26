# SwasthyaSetu

## What This Is

SwasthyaSetu ("Health Bridge") is an AI-powered portable healthcare ecosystem built exclusively for India's 450 million+ internal migrant workers. It bridges gaps in care continuity, language barriers, and occupational health monitoring through a mobile-first, interoperable platform.

## Core Value

Ensure no migrant worker loses healthcare access or goes undiagnosed for occupational diseases due to geography, language, or lack of records.

## Requirements

### Validated

- ✓ **Core Backend Infrastructure** — FastAPI modular monolith, async SQLAlchemy, Pydantic validation
- ✓ **Dual Database Architecture** — PostgreSQL for structured roles/profiles, MongoDB for flexible health records
- ✓ **Local Deployment & Testing** — Dockerized environment with Redis, Redis-backed sessions, 100% passing Pytest suite
- ✓ **Frontend Foundation** — React + Vite boilerplate

### Active

- [ ] **SwasthyaID** — Portable digital health passport via QR and ABHA integration
- [ ] **BhashaSehat** — Multilingual voice AI for symptom input (Whisper + IndicBERT)
- [ ] **KaamSuraksha** — Occupational disease risk prediction engine (XGBoost)
- [ ] **Document AI** — Smart OCR to digitize paper prescriptions and reports
- [ ] **SehatSetu** — Cross-state care continuity and ASHA follow-up assignment
- [ ] **Notify Engine** — Multi-channel alerts (SMS, WhatsApp, IVR)

### Out of Scope

- [Direct Clinical Treatment] — Platform facilitates care logic and predictions but does not replace licensed medical professionals.
- [High-end Smartphone Exclusivity] — Must maintain SMS/IVR fallback because the target demographic uses feature phones.

## Context

- **Target Audience:** Internal migrant workers (India), mostly in high-risk occupations like construction and mining. Low literacy rates; high feature-phone usage.
- **Current State:** Basic architecture is deployed locally. Next phase involves building the core AI modules and ABHA integrations. 

## Constraints

- **Connectivity**: Must be offline-first or resilient to 2G/3G networks.
- **Language**: Voice-first in regional languages (Hindi, Bengali, Tamil, etc.). Must not assume literacy.
- **Privacy**: DPDP Act 2023 compliant. Explicit granular consent required for data sharing.
- **Compute**: AI Models must be optimized for lightweight/frugal inference.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Hybrid Database (PG + Mongo) | Structured RBAC needs relational guarantees; health records need schema flexibility. | ✓ Good |
| FastAPI Backend | High performance, native async support, excellent auto-documentation for integrations. | ✓ Good |

---
*Last updated: March 2026 after initialization*
