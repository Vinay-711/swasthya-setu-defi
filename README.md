<div align="center">

# 🏥 SwasthyaSetu

### *Bridging the Healthcare Gap for India's Invisible Workforce*

**An AI-powered portable healthcare ecosystem for 450 million migrant workers**

---

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.3-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.0-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com)
[![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge)](CONTRIBUTING.md)
[![Hackathon](https://img.shields.io/badge/Built%20For-Hackathon-purple?style=for-the-badge)]()

---

[📋 PRD](docs/PRD.md) · [🛠️ Setup](#-installation) · [🎯 Features](#-core-features) · [🏗️ Architecture](#-system-architecture) · [🤝 Contribute](#-contributing)

</div>

---

## 💔 The Problem We're Solving

> *"A construction worker leaves Bihar for Mumbai. He develops a cough that gets worse every month. He has no health card that works in Maharashtra, no money for a private doctor, no one who speaks his language at the government hospital, and no idea that his job has been slowly destroying his lungs with silica dust."*

**This is not a rare story. This is the daily reality of 450 million migrant workers in India.**

| Statistic | Reality |
|---|---|
| 🏗️ Migrant workers in India | **450 million+** |
| 🏥 With portable health insurance | **< 15%** |
| ☠️ Occupational deaths from undetected disease | **~150,000/year** |
| 📄 Medical records lost during migration | **> 80%** |
| 🗣️ Facing language barriers at clinics | **> 60%** |
| 🫁 Silicosis cases undetected until terminal stage | **> 90%** |

The Indian healthcare system is built for people who stay in one place. Migrant workers — by definition — do not.

---

## 💡 Our Solution

**SwasthyaSetu** (Hindi: *स्वास्थ्यसेतु*, "Health Bridge") is a modular, AI-powered portable healthcare platform that travels *with* the worker, not *against* them.

We give every migrant worker:
- **A health identity that works in any state**
- **A voice that the healthcare system can understand**
- **Records that can't be lost**
- **A system that warns them before their job kills them**

---

## 🎯 Core Features

### 🪪 SwasthyaID — Portable Health Passport
> *One QR. Complete history. Any clinic. Any state.*

- ABHA-linked digital health identity via QR code
- Instant record retrieval at any healthcare facility nationwide
- Granular consent: workers control exactly who sees what
- Works offline; syncs when back online
- ABDM FHIR R4 compliant

---

### 🗣️ BhashaSehat — Voice & Language AI
> *Speak in your language. Be understood.*

- Voice symptom input in **12+ Indian languages** (Hindi, Bengali, Tamil, Telugu, Kannada, Malayalam, Marathi, Gujarati, Odia, Punjabi, Urdu, Assamese)
- OpenAI Whisper fine-tuned for Indian accents + medical vocabulary
- Auto-detects language — no selection needed
- Translates doctor's instructions back to the worker in their native language
- Audio playback for zero-literacy users

---

### 📄 Document AI — Smart OCR
> *Scan a paper prescription. Get a structured digital record.*

- Photograph prescriptions, lab reports, discharge summaries
- Multi-stage OCR: deskew → denoise → extract → structure → translate
- Handles printed AND semi-handwritten prescriptions
- Auto-attached to worker's SwasthyaID profile

---

### ⚠️ KaamSuraksha — Occupational Health AI
> *The only platform in India that predicts job-related diseases before they're irreversible.*

**This is our core USP. Nothing else like it exists in Indian health-tech.**

| Disease | Affected Workers | Currently Detected Early? |
|---|---|---|
| 🫁 Silicosis | Stone quarry, construction, sandblasting | ❌ Almost never |
| 🧵 Byssinosis | Textile mill workers | ❌ Rarely |
| ⛏️ Coal Workers' Pneumoconiosis | Miners | ❌ Rarely |
| 🏭 Occupational Asthma | Chemical factory workers | ❌ No systematic monitoring |
| 🌡️ Heat Stroke Risk | Brick kiln, steel plant workers | ❌ No monitoring |

**How it works:**
1. Worker provides occupation type, years of exposure, specific tasks, PPE usage
2. KaamSuraksha maps this to a hazard exposure profile
3. XGBoost + LightGBM ensemble generates disease probability scores
4. SHAP explainability shows *which factors* drove the risk (clinical trust)
5. Worker gets actionable screening recommendations in their language
6. Employer gets aggregate cluster risk alerts
7. ASHA worker gets screening coordination tasks

---

### 🔄 SehatSetu — Care Continuity System
> *Move to a new city. Your health record arrives before you do.*

- Cross-state health record sync in < 60 seconds
- Auto-assignment of nearest ASHA worker at destination
- Medication adherence tracking via WhatsApp/SMS/IVR
- Chronic disease (TB, diabetes, hypertension) follow-up engine
- Real-time ASHA worker dashboard

---

### 📲 Notify Engine — Multi-Channel Alerts
> *Reach every worker, regardless of phone type or literacy.*

- 📱 WhatsApp rich messages (images, 2-way responses)
- 💬 SMS (works on any phone, even 2G)
- 📞 IVR calls in regional language (zero-literacy support)
- 🔔 Push notifications (Android app)
- Priority fallback: WhatsApp → SMS → IVR

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          CLIENT LAYER                                │
│                                                                      │
│  ┌─────────────────┐  ┌──────────────────┐  ┌───────────────────┐  │
│  │  Android PWA    │  │  ASHA Worker Web  │  │  Feature Phone   │  │
│  │  (Offline-first)│  │    Dashboard      │  │  (IVR / SMS)     │  │
│  └────────┬────────┘  └────────┬──────────┘  └────────┬──────────┘  │
└───────────┼────────────────────┼────────────────────────┼────────────┘
            │                    │                        │
            └───────────────┬────┘────────────────────────┘
                            │ HTTPS / REST / WebSocket
┌───────────────────────────▼───────────────────────────────────────────┐
│                     API GATEWAY (FastAPI)                              │
│          Auth · Rate Limiting · Load Balancing · CORS                 │
└──┬──────────┬───────────┬──────────────┬──────────────┬───────────────┘
   │          │           │              │              │
┌──▼──┐  ┌───▼──┐  ┌─────▼──┐  ┌───────▼──┐  ┌───────▼────────┐
│ ID  │  │Voice │  │Document│  │KaamSu-   │  │SehatSetu +     │
│Svc  │  │  AI  │  │  AI    │  │raksha AI │  │Notify Engine   │
│     │  │      │  │        │  │          │  │                │
│ABHA │  │Whis- │  │Tess-   │  │XGBoost + │  │Celery +        │
│FHIR │  │per + │  │eract + │  │LightGBM +│  │WhatsApp API +  │
│QR   │  │Indic │  │EasyOCR │  │SHAP      │  │SMS + IVR       │
│     │  │BERT  │  │+OpenCV │  │          │  │                │
└──┬──┘  └───┬──┘  └─────┬──┘  └───────┬──┘  └───────┬────────┘
   └─────────┴───────────┴──────────────┴──────────────┘
                          │
          ┌───────────────▼─────────────────┐
          │           DATA LAYER             │
          │  PostgreSQL  │  MongoDB          │
          │  Redis Cache │  S3 (Media)       │
          │  PostGIS     │  (Geospatial)     │
          └───────────────┬─────────────────┘
                          │
          ┌───────────────▼─────────────────┐
          │      EXTERNAL INTEGRATIONS       │
          │  ABHA/ABDM  │  WhatsApp API     │
          │  SMS Gateway │  IVR (Plivo)     │
          │  State Health Portals           │
          └─────────────────────────────────┘
```

---

## 🧠 AI Stack

| Module | Model / Library | Task |
|---|---|---|
| **BhashaSehat ASR** | OpenAI Whisper (fine-tuned) | Speech-to-text, 12 Indian languages |
| **Medical NLP** | IndicBERT / mBERT | Symptom extraction (NER) |
| **Text-to-Speech** | IndicTTS | Regional language audio response |
| **OCR Engine** | Tesseract + EasyOCR | Prescription & report digitization |
| **Image Processing** | OpenCV + scikit-image | Deskew, denoise, binarize |
| **Risk Prediction** | XGBoost + LightGBM | Occupational disease probability |
| **Explainability** | SHAP TreeExplainer | Risk factor attribution (clinical trust) |
| **Geospatial Matching** | PostGIS + geopy | ASHA worker nearest-neighbor assignment |
| **Translation** | IndicTrans2 | Document & instruction translation |

---

## 🛠️ Installation

### Prerequisites

- Python 3.10+
- Node.js 18+ (frontend)
- Docker & Docker Compose
- PostgreSQL 16
- MongoDB 7.0
- Redis 7.2
- Tesseract OCR (system package)

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/your-org/swasthyasetu.git
cd swasthyasetu

# 2. Set up environment variables
cp .env.example .env
# Edit .env with your credentials (ABHA, Twilio, AWS, DB URLs)

# 3. Install system dependencies (Ubuntu/Debian)
sudo apt-get update && sudo apt-get install -y \
  tesseract-ocr \
  tesseract-ocr-hin \
  tesseract-ocr-ben \
  tesseract-ocr-tam \
  libgl1-mesa-glx \
  ffmpeg

# 4. Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 5. Install Python dependencies
pip install -r requirements.txt

# 6. Download AI models
python -m spacy download en_core_web_sm
python scripts/download_models.py   # Downloads Whisper + IndicBERT

# 7. Initialize databases
alembic upgrade head              # PostgreSQL migrations
python scripts/seed_mongodb.py    # MongoDB initial collections

# 8. Start all services with Docker Compose
docker-compose up -d

# 9. Start the backend API
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 10. Start the frontend (separate terminal)
cd frontend
npm install
npm run dev
```

### Docker Compose (Recommended)

```bash
# One-command startup (backend + databases + Redis + Celery)
docker-compose up --build

# API available at:  http://localhost:8000
# API Docs at:       http://localhost:8000/docs
# Frontend at:       http://localhost:3000
# Flower (tasks):    http://localhost:5555
```

### Environment Variables

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/swasthyasetu
MONGODB_URL=mongodb://localhost:27017/swasthyasetu
REDIS_URL=redis://localhost:6379

# ABHA / ABDM Integration
ABHA_BASE_URL=https://healthidsbx.abdm.gov.in/api
ABHA_CLIENT_ID=your_client_id
ABHA_CLIENT_SECRET=your_client_secret

# WhatsApp / SMS
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Cloud Storage
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
S3_BUCKET_NAME=swasthyasetu-documents

# IVR
PLIVO_AUTH_ID=your_plivo_id
PLIVO_AUTH_TOKEN=your_plivo_token

# Security
SECRET_KEY=your-256-bit-secret-key
ALGORITHM=HS256
```

---

## 📖 Usage

### Register a Worker (SwasthyaID)

```bash
curl -X POST http://localhost:8000/api/v1/identity/create \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ramesh Kumar",
    "dob": "1988-05-12",
    "phone": "+919876543210",
    "language": "hi",
    "abha_id": "12-3456-7890-1234",
    "occupation": "construction_worker",
    "years_in_job": 8
  }'
```

### Submit Voice Symptoms (BhashaSehat)

```bash
curl -X POST http://localhost:8000/api/v1/voice/transcribe \
  -H "Authorization: Bearer <token>" \
  -F "audio=@symptom_recording.wav" \
  -F "worker_id=SW-123456"
```

### Get Occupational Risk Profile (KaamSuraksha)

```bash
curl -X POST http://localhost:8000/api/v1/occupational/risk-profile \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "worker_id": "SW-123456",
    "occupation": "stone_quarry_worker",
    "years_in_job": 5,
    "tasks": ["drilling", "blasting", "stone_cutting"],
    "ppe_usage": "rarely",
    "symptoms": ["persistent_cough", "shortness_of_breath"]
  }'
```

**Response:**
```json
{
  "worker_id": "SW-123456",
  "risk_scores": {
    "silicosis": 0.87,
    "byssinosis": 0.04,
    "occupational_asthma": 0.31
  },
  "risk_level": "HIGH",
  "recommendations": [
    "Immediate chest X-ray",
    "Spirometry (lung function test)",
    "Refer to occupational health specialist"
  ],
  "shap_explanation": {
    "top_factors": [
      {"feature": "years_in_job", "impact": 0.42},
      {"feature": "task_stone_cutting", "impact": 0.31},
      {"feature": "ppe_usage_rarely", "impact": 0.28}
    ]
  },
  "alert_sent_to_employer": true,
  "asha_task_created": true
}
```

### Scan a Document (Document AI)

```bash
curl -X POST http://localhost:8000/api/v1/documents/scan \
  -H "Authorization: Bearer <token>" \
  -F "image=@prescription.jpg" \
  -F "worker_id=SW-123456" \
  -F "doc_type=prescription"
```

---

## 📁 Project Structure

```
swasthyasetu/
├── app/
│   ├── main.py                    # FastAPI app entry point
│   ├── core/
│   │   ├── config.py              # Settings & environment
│   │   ├── security.py            # Auth, JWT, encryption
│   │   └── database.py            # DB connection managers
│   ├── api/
│   │   └── v1/
│   │       ├── identity.py        # SwasthyaID endpoints
│   │       ├── voice.py           # BhashaSehat endpoints
│   │       ├── documents.py       # Document AI endpoints
│   │       ├── occupational.py    # KaamSuraksha endpoints
│   │       ├── continuity.py      # SehatSetu endpoints
│   │       └── notifications.py   # Notify Engine endpoints
│   ├── models/
│   │   ├── worker.py              # SQLAlchemy worker model
│   │   ├── health_record.py       # Health record model
│   │   └── occupational_risk.py   # Risk profile model
│   ├── services/
│   │   ├── voice_ai/
│   │   │   ├── whisper_engine.py  # ASR service
│   │   │   ├── indic_nlp.py       # Symptom extraction
│   │   │   └── tts_engine.py      # Text-to-speech
│   │   ├── document_ai/
│   │   │   ├── ocr_pipeline.py    # OCR orchestration
│   │   │   ├── image_preprocessor.py
│   │   │   └── record_extractor.py
│   │   ├── kaamsurakhsha/
│   │   │   ├── risk_model.py      # XGBoost inference
│   │   │   ├── explainer.py       # SHAP explanations
│   │   │   └── training/
│   │   │       ├── train.py       # Model training pipeline
│   │   │       └── evaluate.py    # AUC-ROC evaluation
│   │   ├── continuity/
│   │   │   ├── location_sync.py   # Cross-state record sync
│   │   │   └── asha_matcher.py    # Geospatial ASHA assignment
│   │   └── notifications/
│   │       ├── whatsapp.py        # WhatsApp Business API
│   │       ├── sms.py             # SMS gateway
│   │       └── ivr.py             # IVR (Plivo)
│   └── tasks/
│       ├── celery_app.py          # Celery configuration
│       └── scheduled_tasks.py     # Daily risk score updates
├── frontend/                      # React.js frontend
├── models/                        # Trained model artifacts (.pkl, .pt)
├── data/
│   └── occupational/              # Training datasets (anonymized)
├── migrations/                    # Alembic DB migrations
├── tests/
│   ├── unit/
│   └── integration/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs/
│   ├── PRD.md
│   ├── API.md
│   └── ARCHITECTURE.md
├── requirements.txt
├── .env.example
└── README.md
```

---

## 💰 Business Model

| Revenue Stream | Description | Target |
|---|---|---|
| 🏛️ **Government Contracts** | Outcome-based SLAs with State NHM | ₹50L–5Cr per state/year |
| 🏗️ **Employer Subscriptions** | Per-worker annual plan for factories/construction | ₹200–500/worker/year |
| 💳 **Pay-Per-Use** | Per scan / record access | ₹5–10 per transaction |
| 🌐 **Public Health Grants** | Gates Foundation, USAID, WHO India | Project-based |
| 📊 **Anonymized Data Insights** | Aggregated health trends for research / insurance | ₹5L–50L per dataset |
| 🤝 **CSR Funding** | Worker health programs under 2% CSR mandate | ₹25L–5Cr per company |

---

## 🌍 Why This Matters

> **450 million people are invisible to India's healthcare system. SwasthyaSetu makes them visible.**

- Every ₹1 spent on early occupational disease detection saves ₹8–12 in terminal care costs
- Silicosis is 100% preventable — but kills tens of thousands because no one monitors risk
- Digital health identity unlocks Ayushman Bharat for workers currently excluded by state-boundary rules
- ASHA workers have no tools to follow up with patients who move — we give them those tools

**This is not just health-tech. This is a justice issue wrapped in a technology solution.**

---

## 📊 Impact Targets

| Metric | 6 Months | 18 Months | 3 Years |
|---|---|---|---|
| Workers enrolled | 10,000 | 500,000 | 10,000,000 |
| Occupational diseases caught early | 200 | 10,000 | 200,000 |
| Documents digitized | 50,000 | 2,000,000 | 50,000,000 |
| States deployed | 2 | 12 | 28 |
| Languages supported | 5 | 12 | 18 |

---

## 🔭 Future Roadmap

- [ ] **v1.0** — SwasthyaID + KaamSuraksha (silicosis, byssinosis) + Hindi/Bengali/Tamil
- [ ] **v1.5** — Document AI + 12-language BhashaSehat + SehatSetu
- [ ] **v2.0** — KaamSuraksha v2 (CWP, NIHL, chemical poisoning) + iOS app
- [ ] **v2.5** — Telemedicine integration (regional language video consult)
- [ ] **v3.0** — Federated learning across states + Blockchain consent audit trail
- [ ] **v3.5** — International migrant workers (Gulf, Southeast Asia)
- [ ] **v4.0** — SwasthyaSetu API marketplace for third-party health-tech

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v --cov=app --cov-report=html

# Run specific module tests
pytest tests/unit/test_kaamsurakhsha.py -v
pytest tests/integration/test_voice_ai.py -v

# Check coverage
open htmlcov/index.html
```

---

## 🤝 Contributing

We welcome contributions, especially from:
- **AI/ML Engineers** — Improve KaamSuraksha models, add new disease predictions
- **NLP Specialists** — Expand BhashaSehat to more Indian languages
- **Public Health Researchers** — Validate occupational risk models with field data
- **Designers** — Improve low-literacy UX for the Android app

```bash
# Fork the repo → Create a feature branch
git checkout -b feature/add-pneumoconiosis-model

# Make your changes → Write tests → Submit PR
git push origin feature/add-pneumoconiosis-model
```

Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

## 👥 Team

| Role | Responsibility |
|---|---|
| 🧑‍💻 **AI/ML Lead** | KaamSuraksha models, BhashaSehat ASR |
| 🧑‍💻 **Backend Lead** | FastAPI microservices, ABHA integration |
| 🧑‍🎨 **Frontend Lead** | React PWA, ASHA worker dashboard |
| 🧑‍⚕️ **Domain Expert** | Occupational health dataset curation, clinical validation |
| 📊 **Product/Data** | PRD, KPI tracking, anonymized analytics |

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- **Ministry of Health & Family Welfare (MOHFW)** — ABHA/ABDM open APIs
- **AI4Bharat** — IndicBERT, IndicTTS, IndicTrans2 open-source models
- **National Institute for Occupational Safety & Health (NIOSH)** — Occupational disease datasets
- **OpenAI** — Whisper open-source ASR model
- **Jan Sahas, Aajeevika Bureau** — Ground-truth data on migrant worker health

---

<div align="center">

**Built with ❤️ for India's invisible workforce**

*"स्वास्थ्य सबका अधिकार है।" — Health is everyone's right.*

[![GitHub stars](https://img.shields.io/github/stars/your-org/swasthyasetu?style=social)](https://github.com/your-org/swasthyasetu)
[![Twitter Follow](https://img.shields.io/twitter/follow/SwasthyaSetu?style=social)](https://twitter.com/SwasthyaSetu)

</div>
