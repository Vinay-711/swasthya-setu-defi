# Architecture Map

## Pattern
- **Modular Monolith**: The backend is organized into domain-specific modules inside `app/` (e.g., `api`, `models`, `services`, `core`).

## Data Flow
- **Request Lifecycle**: Client -> FastAPI Endpoints (`app/api/`) -> Business Logic (`app/services/`) -> Async SQLAlchemy DB Session -> PostgreSQL/MongoDB.
- **Caching/State**: Redis used for session management and transient state.

## Entry Points
- **Backend API**: `backend/app/main.py` is the FastAPI application entry point.
- **Database Migrations**: Alembic via `alembic/env.py`.
- **Infrastructure**: `docker-compose.yml` orchestrates the local deployment.
