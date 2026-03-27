# SwasthyaSetu Architecture Plan

## 1. Core Services

- **FastAPI Backend** (`backend/app`): modular routers + service layer + AI modules.
- **React Frontend** (`frontend/src`): authenticated dashboard with module pages.
- **PostgreSQL**: system of record for users, records, risk, documents, notifications, tracking.
- **MongoDB**: unstructured document payload mirror for analytics.
- **Redis**: notification event queue simulation.

## 2. Backend Layers

- `routes/`: transport layer (HTTP endpoints).
- `services/`: business logic.
- `models/`: SQLAlchemy models.
- `schemas/`: request/response validation.
- `ai_modules/`: BhashaSehat, Document AI, KaamSuraksha logic.
- `core/`: config, auth security, dependencies, logging.
- `utils/`: encryption, ID generation, QR helpers.

## 3. Frontend Modules

- Auth + token storage.
- Dashboard + quick actions.
- QR lookup page.
- Document upload page.
- KaamSuraksha risk page with animated score + SHAP bars.
- Worker tracking + timeline.
- Worker clinic record page.

## 4. Security

- JWT access tokens.
- Role-based dependency guards.
- Encrypted phone storage (Fernet).
- Consent check for worker record access.

## 5. DevOps

- Dockerfiles for backend and frontend.
- Docker Compose with `postgres`, `mongodb`, `redis`, `pgadmin`, and network `swasthya-net`.
- Alembic migration baseline in `backend/alembic/versions`.
- pytest suite for health/auth/risk/AI logic.
