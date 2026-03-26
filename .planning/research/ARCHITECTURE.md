# Domain Research: Architecture (Occupational Migrant Health)

## System Structure
- **Client Layer**: Offline-first Next.js PWA or React Vite SPA. Worker and ASHA facing.
- **Gateway**: FastAPI routing with JWT/OAuth2 RBAC.
- **Microservices Organization**:
  - `Identity Service`: SwasthyaID / ABHA integration.
  - `Voice AI Service`: Audio handling and transcriptions.
  - `Occupational AI Service`: ML predictions and risk scoring.
  - `Notification Service`: Async Celery/Redis workers pushing to Twilio/WhatsApp APIs.
- **Storage Layer**: PostgreSQL for structured data (profiles, identities) and MongoDB for flexible unstructured documents (prescriptions, changing symptom schemas).

## Data Flow
Worker -> Voice Input -> Whisper API -> Intent/Symptom NLP -> PostgreSQL/MongoDB -> Async Risk Trigger -> Celery Task -> SMS/IVR Alert.
