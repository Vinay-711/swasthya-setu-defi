# SwasthyaSetu — Product Requirements Document (PRD)

> **Version:** 1.0 | **Status:** Active Development | **Date:** March 2026
> **Prepared by:** SwasthyaSetu Product Team

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Target Users](#3-target-users)
4. [Solution Overview](#4-solution-overview)
5. [Feature Breakdown](#5-feature-breakdown)
6. [User Flow](#6-user-flow)
7. [System Architecture](#7-system-architecture)
8. [AI Components](#8-ai-components)
9. [Data Privacy & Security](#9-data-privacy--security)
10. [Scalability Strategy](#10-scalability-strategy)
11. [Business Model](#11-business-model)
12. [Success Metrics (KPIs)](#12-success-metrics-kpis)
13. [Future Roadmap](#13-future-roadmap)

---

## 1. Executive Summary

SwasthyaSetu ("Health Bridge" in Hindi) is an AI-powered portable healthcare ecosystem built exclusively for India's 450 million+ internal migrant workers — one of the world's most medically underserved populations.

Migrant workers face a structural healthcare gap: they move across states for work, lose access to local health schemes, carry paper records that get lost, struggle with language barriers at clinics, and face severe occupational health risks with zero systematic monitoring. SwasthyaSetu eliminates every one of these barriers through six deeply integrated modules:

| Module | Purpose |
|---|---|
| **SwasthyaID** | Portable digital health passport via QR + ABHA |
| **BhashaSehat** | Multilingual voice AI for symptom input |
| **Document AI** | Smart OCR to digitize paper prescriptions & reports |
| **KaamSuraksha** | Occupational disease risk prediction (core USP) |
| **SehatSetu** | Cross-state care continuity & ASHA follow-up |
| **Notify Engine** | SMS / WhatsApp / IVR alerts & reminders |

SwasthyaSetu is designed to be deployed by state governments, CSR wings of large employers (construction, textiles, mining), and NGOs — with a B2G2C (Business to Government to Consumer) go-to-market model.

---

## 2. Problem Statement

### 2.1 Scale of the Crisis

- **450 million+** internal migrants in India (Census 2011 projection; estimated 600M+ post-2020)
- **70%** work in high-risk industries: construction, brick kilns, textile mills, mining, domestic work
- **<15%** have any form of health insurance that works across state borders
- **80%** of occupational diseases in India go undiagnosed until terminal stages
- Silicosis alone kills **~10,000 workers per year** in India; byssinosis, CWP, and other occupational diseases claim tens of thousands more

### 2.2 Root Causes

| Problem | Impact |
|---|---|
| No portable health identity | Lose access to Ayushman Bharat and state schemes on relocation |
| Language barriers | Cannot communicate symptoms accurately at destination clinics |
| Paper-based records | Lost during migration; no continuity of care |
| Zero occupational risk monitoring | Diseases detected only at irreversible stages |
| Low digital literacy | Cannot use standard health apps or portals |
| No ASHA / community worker reach | Follow-up impossible after workers move |

### 2.3 Why This Is Urgent Now

- India's National Health Policy 2017 mandates universal health coverage, yet migrant workers remain structurally excluded
- ABHA (Ayushman Bharat Health Account) exists but lacks a migrant-specific layer
- 5G & Jan Dhan / UPI penetration now makes a mobile-first solution viable even in semi-urban areas

---

## 3. Target Users

### Primary Users

**Migrant Workers**
- Age: 18–55 | Education: Often class 8 or below | Languages: 12+ regional
- Tech comfort: Feature phone / entry-level Android; WhatsApp-native
- Needs: Access care, carry records, communicate in native language, get medication reminders

### Secondary Users

**Employers (Factories, Construction Companies)**
- Need: Compliance with Occupational Safety, Health & Working Conditions Code 2020; CSR reporting; workforce productivity
- Value: Risk dashboards, aggregate health reports, reduced liability

**Government Bodies**
- MOHFW, State Health Departments, NHM (National Health Mission)
- Need: Surveillance data, outbreak alerts, outcome metrics for scheme evaluation

**Healthcare Providers**
- PHCs, district hospitals, private clinics
- Need: Patient history on first visit, language-bridged consultation, digitized records

**ASHA / Community Health Workers**
- Need: Worker location tracking, follow-up alerts, care coordination tools

---

## 4. Solution Overview

SwasthyaSetu operates as a progressive web app (PWA) and lightweight Android APK, backed by a Python FastAPI microservices backend with specialized AI models for each module. The platform is ABHA-integrated, works on 2G/3G networks with offline-first caching, and supports both smartphone and feature-phone (IVR/SMS) access paths.

### Design Principles

1. **Offline-first:** Core features work without internet; sync when connected
2. **Language-first:** Never assume literacy; voice is the primary input
3. **Privacy-by-design:** Consent gates on all record access
4. **Interoperable:** Plug into ABHA, state health systems, and employer HR systems via open APIs
5. **Frugal compute:** Models optimized for edge/low-resource inference

---

## 5. Feature Breakdown

### 5.1 SwasthyaID — Portable Health Passport

**Goal:** Give every migrant worker a persistent, portable, privacy-respecting digital health identity that works across all 28 states.

**Functional Requirements:**

- Generate a unique SwasthyaID linked to ABHA ID upon registration
- Store and retrieve: demographics, chronic conditions, allergies, vaccination history, past diagnoses, medications, emergency contacts
- QR code for instant identity sharing at any clinic or hospital
- Role-based access control (RBAC): worker consents to share specific records with a specific provider for a limited time
- Works offline; syncs when connectivity resumes
- Support biometric (fingerprint/face) and PIN-based authentication

**Non-Functional Requirements:**

- QR scan to record retrieval: < 2 seconds
- Zero-knowledge encryption for sensitive fields
- ABDM (Ayushman Bharat Digital Mission) FHIR R4 compliance

**APIs:**
- `POST /api/v1/identity/create` — register new worker
- `GET /api/v1/identity/{swasthya_id}/qr` — generate QR
- `POST /api/v1/identity/verify` — clinic-side verification
- `PUT /api/v1/identity/{swasthya_id}/consent` — grant/revoke record access

---

### 5.2 BhashaSehat — Voice & Language AI

**Goal:** Allow any worker, regardless of literacy level or language, to interact with the platform naturally using voice in their mother tongue.

**Functional Requirements:**

- Voice symptom capture in 12+ languages: Hindi, Bengali, Tamil, Telugu, Kannada, Malayalam, Marathi, Gujarati, Odia, Punjabi, Urdu, Assamese
- Real-time speech-to-text using OpenAI Whisper (fine-tuned for Indian accents and medical terminology)
- Symptom extraction using IndicBERT / fine-tuned Bio-BERT for Indian medical NLP
- Text-to-speech response playback in user's language
- Auto-detect language from speech (no language selection required)
- Translate clinical instructions from provider into worker's language
- Low-bandwidth audio compression for 2G compatibility

**Non-Functional Requirements:**

- Speech recognition accuracy: >90% on Indian-accented Hindi/Bengali/Tamil
- Latency from voice input to response: <4 seconds on 3G
- Minimum supported audio quality: 8kHz mono (feature phone standard)

**APIs:**
- `POST /api/v1/voice/transcribe` — audio → text + detected language
- `POST /api/v1/voice/synthesize` — text → audio in target language
- `POST /api/v1/voice/extract-symptoms` — NLP symptom extraction from transcript

---

### 5.3 Document AI — Smart OCR

**Goal:** Convert paper prescriptions, lab reports, and discharge summaries into structured, searchable digital records automatically.

**Functional Requirements:**

- Scan via smartphone camera or upload image/PDF
- OCR pipeline: image pre-processing (deskew, denoise, binarize) → text extraction → structured parsing
- Support printed and semi-handwritten prescriptions
- Extract: drug name, dosage, frequency, duration, lab values, diagnosis codes
- Auto-translate extracted content to worker's preferred language
- Flag illegible sections and prompt for manual review
- Attach digitized records to the worker's SwasthyaID profile

**Non-Functional Requirements:**

- OCR accuracy on clear printed prescriptions: >92%
- Processing time per document: <8 seconds
- Support image formats: JPG, PNG, HEIC, PDF

**APIs:**
- `POST /api/v1/documents/scan` — upload image, returns structured JSON
- `GET /api/v1/documents/{doc_id}` — retrieve processed document
- `POST /api/v1/documents/{doc_id}/translate` — translate extracted text

---

### 5.4 KaamSuraksha — Occupational Health AI ⭐ CORE USP

**Goal:** Proactively detect and predict occupational disease risk before it becomes irreversible, using a worker's job profile, duration of exposure, symptoms, and location.

**Why This Is the USP:** No existing Indian health platform — public or private — does systematic, AI-driven occupational disease risk prediction for informal sector workers. This is a genuine market whitespace with life-saving potential.

**Functional Requirements:**

**Risk Profiling Engine:**
- Intake: occupation type, years in current job, industry, specific tasks (e.g., sandblasting, weaving, mining), use of PPE
- Map occupation to hazard exposure profile (dust, chemicals, noise, heat, vibration)
- Generate a Risk Score (0–100) for each hazard category

**Disease Prediction Models:**
| Disease | Primary Trigger | Population at Risk |
|---|---|---|
| Silicosis | Crystalline silica dust | Stone quarry, construction, sandblasting workers |
| Byssinosis | Cotton/textile dust | Mill and weaving workers |
| Coal Workers' Pneumoconiosis | Coal dust | Mining workers |
| Occupational Asthma | Chemical fumes | Paint, chemical factory workers |
| Heat Stroke | High-temperature environments | Brick kiln, steel plant workers |
| Noise-Induced Hearing Loss | Chronic noise exposure | Manufacturing, construction workers |
| Chemical Poisoning | Pesticide / solvent exposure | Agricultural, dry cleaning workers |

**Screening Recommendation Engine:**
- Based on risk score + time in job, recommend specific screenings (chest X-ray, spirometry, audiometry, blood tests)
- Generate referral letters pre-filled with worker's exposure history
- Alert employer's safety officer if cluster of high-risk workers detected

**Preventive Guidance:**
- PPE recommendations in worker's language
- Job-specific safety tips via voice/WhatsApp
- Seasonal risk alerts (e.g., increased silicosis risk during dry season in quarry work)

**Non-Functional Requirements:**

- Model: Gradient Boosted Trees (XGBoost/LightGBM) + lightweight neural layer
- Training data: NIN (National Institute of Nutrition) occupational health datasets, peer-reviewed Indian epidemiological studies, WHO occupational disease burden data
- Prediction latency: <1 second
- Model explainability: SHAP values for each risk factor (required for clinical trust)

**APIs:**
- `POST /api/v1/occupational/risk-profile` — submit work history, get risk scores
- `GET /api/v1/occupational/recommendations/{worker_id}` — screening recommendations
- `POST /api/v1/occupational/cluster-alert` — employer-level aggregate risk alert
- `GET /api/v1/occupational/explain/{risk_id}` — SHAP-based explanation

---

### 5.5 SehatSetu — Care Continuity System

**Goal:** Ensure that a worker who moves from Mumbai to Surat does not fall off the healthcare radar, losing their treatment history and follow-up care.

**Functional Requirements:**

- Location-aware health record sync: when worker registers at a new location, their complete record is available within 60 seconds
- ASHA worker assignment: auto-assign nearest available ASHA worker at destination location
- Follow-up scheduler: generate post-visit follow-up reminders for worker and ASHA worker
- Medication adherence tracking: worker confirms medication intake via WhatsApp/SMS/IVR
- Chronic disease management: monthly check-in prompts for workers with diabetes, hypertension, TB
- Referral tracking: log referrals and flag if worker doesn't attend within 72 hours
- Dashboard for ASHA workers: list of assigned migrant workers, pending follow-ups, overdue medications

**Non-Functional Requirements:**

- Data sync latency across states: <60 seconds
- ASHA worker app must function on 3G with 50KB/s bandwidth
- Support 10,000 concurrent ASHA worker sessions

**APIs:**
- `PUT /api/v1/continuity/location/{worker_id}` — update worker location
- `GET /api/v1/continuity/asha-assignments/{district_code}` — ASHA worker dashboard
- `POST /api/v1/continuity/followup` — create follow-up task
- `POST /api/v1/continuity/adherence/{worker_id}` — log medication adherence

---

### 5.6 Notification Engine

**Goal:** Reach workers through every available channel, prioritizing the most accessible for their context.

**Functional Requirements:**

- **SMS:** Appointment reminders, medication alerts, screening due notices — works on any phone
- **WhatsApp:** Rich notifications with images (PPE guides, screening instructions), 2-way responses ("Reply 1 to confirm your appointment")
- **IVR (Interactive Voice Response):** Automated phone calls in regional language for zero-literacy users; press-key navigation
- **Push Notifications:** For smartphone app users
- **Priority Routing:** If WhatsApp fails, fall back to SMS; if SMS undelivered, trigger IVR call

**Notification Types:**
- Medication reminder (daily/twice-daily)
- Appointment confirmation & reminder
- Screening due alert (occupational health)
- ASHA follow-up alert
- Health scheme enrollment eligibility alert
- Emergency contact notification

---

## 6. User Flow

### 6.1 New Worker Onboarding Flow

```
Worker arrives at worksite / clinic
       │
       ▼
ASHA worker / employer HR scans → Opens SwasthyaSetu app
       │
       ▼
Voice onboarding in regional language (BhashaSehat)
"Aapka naam kya hai? Aap kahan se aaye hain?"
       │
       ▼
SwasthyaID created → Linked to ABHA (if existing) or new ABHA generated
       │
       ▼
Occupation intake form → KaamSuraksha risk profile generated
       │
       ▼
QR code issued (printed sticker or saved to phone)
       │
       ▼
Notification preferences set (WhatsApp / SMS / IVR)
       │
       ▼
Worker is onboarded ✓
```

### 6.2 Clinic Visit Flow

```
Worker arrives at PHC / hospital
       │
       ▼
Shows QR code at reception
       │
       ▼
Clinic staff scans QR → Complete health history displayed in seconds
       │
       ▼
Doctor consults → Prescription written
       │
       ▼
Document AI: Prescription photographed → digitized → added to SwasthyaID
       │
       ▼
BhashaSehat: Doctor's instructions translated to worker's language + audio playback
       │
       ▼
SehatSetu: Follow-up appointment scheduled → Notify Engine sends reminders
       │
       ▼
Medication adherence tracking begins
```

### 6.3 Occupational Risk Alert Flow

```
Worker completes occupation history
       │
       ▼
KaamSuraksha computes risk score
       │
       ▼
[If High Risk → Score > 70]
       │
       ▼
Worker receives voice alert: "Aapke kaam mein silicosis ka khatra hai"
       │
       ▼
Recommended screening list generated
       │
       ▼
Employer safety officer receives aggregate cluster alert
       │
       ▼
ASHA worker receives task: arrange chest X-ray for flagged workers
       │
       ▼
Results logged → Risk score recalculated
```

---

## 7. System Architecture

### 7.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                          │
│   Android APK (Offline-First PWA)  │  Feature Phone (IVR)  │
│   ASHA Worker Web Dashboard        │  WhatsApp Bot          │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS / REST / WebSocket
┌──────────────────────▼──────────────────────────────────────┐
│                     API GATEWAY (FastAPI)                     │
│   Auth (JWT + OAuth2)  │  Rate Limiting  │  Load Balancer   │
└──┬─────────┬──────────┬──────────┬───────────────────┬──────┘
   │         │          │          │                   │
┌──▼──┐  ┌──▼──┐  ┌────▼───┐  ┌──▼──────┐  ┌────────▼──────┐
│ ID  │  │Voice│  │Document│  │KaamSu-  │  │SehatSetu /     │
│Svc  │  │ AI  │  │  AI    │  │raksha   │  │Notify Engine   │
└──┬──┘  └──┬──┘  └────┬───┘  └──┬──────┘  └────────┬──────┘
   │         │          │          │                   │
┌──▼─────────▼──────────▼──────────▼───────────────────▼──────┐
│                    DATA LAYER                                  │
│  PostgreSQL (structured) │ MongoDB (documents/records)        │
│  Redis (caching/sessions) │ S3/GCS (media, scanned docs)     │
└────────────────────────────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│               EXTERNAL INTEGRATIONS                          │
│  ABHA / ABDM APIs  │  WhatsApp Business API  │  SMS Gateway │
│  IVR Provider      │  State Health Portals                  │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Microservices Breakdown

| Service | Tech | Responsibility |
|---|---|---|
| Identity Service | FastAPI + PostgreSQL | SwasthyaID lifecycle, ABHA linking, QR |
| Voice AI Service | FastAPI + Whisper + IndicBERT | ASR, TTS, NLP |
| Document AI Service | FastAPI + Tesseract/EasyOCR + OpenCV | OCR, extraction |
| Occupational AI Service | FastAPI + XGBoost + SHAP | Risk scoring, prediction |
| Continuity Service | FastAPI + MongoDB | Location sync, care tracking |
| Notification Service | FastAPI + Celery | Multi-channel alert routing |
| Auth Service | FastAPI + OAuth2 | JWT, RBAC, consent management |

---

## 8. AI Components

### 8.1 Speech Recognition (BhashaSehat)
- **Model:** OpenAI Whisper (medium) fine-tuned on IndicSuperb dataset for 12 Indian languages
- **Medical vocabulary fine-tuning:** domain-specific vocabulary on Indian prescription language
- **Output:** Transcript + language tag + confidence score
- **Fallback:** If confidence < 0.7, prompt user to repeat or switch to text input

### 8.2 Medical NLP (BhashaSehat)
- **Model:** IndicBERT or mBERT fine-tuned on symptom extraction tasks
- **Task:** Named Entity Recognition (NER) for symptoms, body parts, durations
- **Output:** Structured symptom JSON `{"symptom": "chest pain", "duration": "3 days", "severity": "moderate"}`

### 8.3 OCR Pipeline (Document AI)
- **Stage 1 – Pre-processing:** OpenCV (deskew, denoise, binarize, contrast enhancement)
- **Stage 2 – Text Extraction:** Tesseract (printed) + EasyOCR (semi-handwritten)
- **Stage 3 – Structure Parsing:** Regex + spaCy NER for medication extraction
- **Stage 4 – Translation:** IndicTrans2 for cross-lingual output

### 8.4 Occupational Risk Model (KaamSuraksha)
- **Algorithm:** XGBoost Classifier (primary) + LightGBM (ensemble validation)
- **Features:**
  - Occupation type (encoded), years in job, industry sector
  - Specific task categories (dust-generating, chemical-handling, etc.)
  - PPE usage frequency
  - Reported symptoms (from BhashaSehat integration)
  - Geographic region (environmental exposure proxy)
- **Target Variables:** Probability of silicosis, byssinosis, CWP, occupational asthma (multi-label)
- **Explainability:** SHAP TreeExplainer for per-prediction feature attribution
- **Model Validation:** 5-fold cross-validation; target AUC-ROC > 0.85 per disease
- **Retraining Cadence:** Monthly, with new screening outcome data

### 8.5 Care Continuity Intelligence (SehatSetu)
- **Rule-based + ML:** Medication adherence pattern detection using time-series analysis
- **Alert Logic:** Configurable threshold-based triggers (e.g., 3 consecutive missed doses → ASHA alert)
- **ASHA Assignment:** Nearest-neighbor geospatial matching using PostGIS

---

## 9. Data Privacy & Security

### 9.1 Regulatory Compliance
- **DPDP Act 2023 (Digital Personal Data Protection):** Full compliance; consent-first architecture
- **ABDM Data Policy:** FHIR R4 standard for health records
- **IT Act 2000:** Data localization on Indian cloud regions

### 9.2 Consent Architecture
- **Granular consent:** Worker consents to share specific record categories (prescriptions vs. diagnoses vs. occupational data) with specific entities (clinic vs. employer vs. government) for a defined time window
- **Consent audit log:** Every access to a worker's record is logged with timestamp, accessor identity, and purpose
- **Right to withdraw:** Worker can revoke consent at any time via WhatsApp ("STOP SHARE") or app

### 9.3 Encryption & Access Control
- **At rest:** AES-256 encryption for all PII fields in database
- **In transit:** TLS 1.3 for all API communication
- **Zero-knowledge fields:** Sensitive diagnoses (e.g., HIV, TB) stored with additional field-level encryption; never included in employer-facing reports
- **RBAC:** Role-based access — worker, ASHA worker, clinic provider, employer safety officer, government analyst — each with strictly scoped permissions

### 9.4 Anonymization for Research/Analytics
- **k-anonymity (k≥5):** Aggregate analytics; no individual can be identified
- **Differential privacy:** Applied on population-level health insight exports
- **De-identification:** All research data exports strip 18 HIPAA-equivalent direct identifiers

### 9.5 Infrastructure Security
- Cloud-native VPC with private subnets for all databases
- WAF (Web Application Firewall) on API gateway
- Penetration testing quarterly; VAPT before each major release
- SIEM (Security Information and Event Management) for real-time threat detection

---

## 10. Scalability Strategy

### 10.1 Technical Scalability
- **Horizontal scaling:** All microservices containerized (Docker) and orchestrated via Kubernetes; auto-scaling based on CPU/request load
- **Database sharding:** PostgreSQL partitioned by state/region; MongoDB sharded collections for document records
- **CDN:** Static assets and frequently accessed QR codes served via CloudFront/Azure CDN
- **Message queue:** Celery + Redis for async notification delivery; handles 1M+ messages/day
- **AI model serving:** TorchServe / ONNX Runtime for low-latency inference; GPU instances for training, CPU for inference

### 10.2 Geographic Scalability
- Multi-region cloud deployment (3 Indian regions: Mumbai, Chennai, Delhi NCR) for low latency and data residency compliance
- State-specific data partitions for compliance with state health data policies
- Offline-sync architecture ensures functionality in network-poor areas (brick kilns, remote worksites)

### 10.3 User Scalability Targets

| Phase | Workers | Daily Active Users | Notifications/Day |
|---|---|---|---|
| MVP (Month 0–6) | 10,000 | 2,000 | 50,000 |
| Scale (Month 6–18) | 500,000 | 100,000 | 2,000,000 |
| National (Month 18–36) | 10,000,000 | 2,000,000 | 50,000,000 |

---

## 11. Business Model

### Revenue Streams

**1. Outcome-Based Government Funding**
- SLA-based contracts with state NHM offices: payment tied to workers enrolled, screenings completed, and diseases detected early
- Central government (MOHFW) grants under PMGDISHA and Ayushman Bharat Digital Mission
- Estimated per-state contract: ₹50 lakh – ₹5 crore per year

**2. Employer-Paid Model**
- Construction companies, textile mills, mining firms pay a per-worker annual subscription
- Value proposition: OSH Code 2020 compliance, reduced liability, CSR reporting
- Pricing: ₹200–500 per worker per year (B2B SaaS)
- Target customers: L&T, Tata Projects, GMR, JK Cement, and 200,000+ unorganized employers

**3. Pay-Per-Use**
- Individual scan: ₹10 per document digitization
- Record access by clinic: ₹5 per worker record access (API)
- Premium features: ₹49/month for advanced medication tracking

**4. Government Grants & Public Health Funding**
- Gates Foundation, Wellcome Trust, USAID, WHO India
- National Health Authority (NHA) pilot grants
- MeitY's Digital India grants for health-tech

**5. Anonymized Health Insights (B2B)**
- De-identified, aggregated occupational health trend data sold to:
  - Pharmaceutical companies for drug demand forecasting
  - Insurance companies for actuarial risk modeling
  - Public health researchers
- Pricing: ₹5–50 lakh per research dataset

**6. CSR Funding**
- Mandatory 2% CSR spend by companies employing 500+ workers
- Packaged as "Worker Health & Dignity Program" — a ready CSR narrative for companies
- Target companies: Adani Group, Tata, Mahindra, ITC, JSW, ACC Cement
- Estimated CSR deal size: ₹25 lakh – ₹5 crore per company

---

## 12. Success Metrics (KPIs)

### Impact Metrics
| Metric | 6-Month Target | 18-Month Target |
|---|---|---|
| Workers registered on SwasthyaID | 10,000 | 500,000 |
| High-risk workers screened via KaamSuraksha | 2,000 | 100,000 |
| Occupational diseases detected early | 200 | 10,000 |
| Documents digitized via Document AI | 50,000 | 2,000,000 |
| Medication adherence rate (SehatSetu) | 60% | 75% |
| States with active SwasthyaSetu deployments | 2 | 12 |

### Product Metrics
| Metric | Target |
|---|---|
| SwasthyaID QR verification time | < 2 seconds |
| Voice recognition accuracy (Hindi) | > 90% |
| OCR accuracy (printed prescriptions) | > 92% |
| KaamSuraksha risk model AUC-ROC | > 0.85 |
| App uptime (SLA) | 99.5% |
| Notification delivery rate | > 95% |

### Business Metrics
| Metric | 12-Month Target |
|---|---|
| Government contracts signed | 3 states |
| Employer partnerships | 50 companies |
| ARR (Annual Recurring Revenue) | ₹2 crore |
| CSR grants secured | ₹1 crore |
| Cost per worker onboarded | < ₹150 |

---

## 13. Future Roadmap

### Phase 1 — MVP (Months 0–6)
- SwasthyaID + QR + ABHA linking
- BhashaSehat (Hindi + Bengali + Tamil)
- KaamSuraksha v1 (silicosis + byssinosis prediction)
- WhatsApp + SMS notifications
- ASHA worker web dashboard

### Phase 2 — Scale (Months 6–18)
- Full 12-language support in BhashaSehat
- Document AI (prescription + lab report digitization)
- SehatSetu care continuity across 5+ states
- Employer safety dashboard with aggregate risk views
- IVR system for zero-literacy users
- iOS app (employer/provider facing)

### Phase 3 — Platform (Months 18–36)
- National rollout (15+ states)
- Integration with Co-WIN, e-Sanjeevani, state health portals
- KaamSuraksha v2: CWP, noise-induced hearing loss, chemical poisoning models
- Telemedicine integration (worker → doctor in regional language via video)
- Federated learning across states for model improvement without data centralization
- Blockchain-based consent audit trail (immutable, verifiable)
- SwasthyaSetu API marketplace for third-party health-tech builders

### Phase 4 — Expansion (Months 36+)
- International migrant workers: Gulf countries, Southeast Asia
- Occupational health insurance product (partnered with insurer)
- AI-powered epidemiological surveillance for state governments
- Integration with National Occupational Health Registry (once established)
