# Codebase Structure

## Root Directory
- `/backend`: The Python FastAPI application and its tests.
- `/frontend`: The React application (Vite).
- `/scripts`: Utility scripts, such as database seeding (`seed_mongodb.py`).
- `docker-compose.yml`: Local infrastructure definition.

## Backend Structure (`/backend/app`)
- `/api`: FastAPI route definitions and endpoints.
- `/core`: Application configuration, security utilities, and base settings.
- `/models`: SQLAlchemy ORM models (e.g., `health_record.py`).
- `/schemas`: Pydantic definitions for request/response validation.
- `/services`: Core business logic (e.g., identity, document AI).
- `/tests`: Pytest suite.

## Key Naming Conventions
- Database models use PascalCase (`HealthRecord`).
- Endpoints and core modules use snake_case.
