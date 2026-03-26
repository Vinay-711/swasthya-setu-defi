# Phase 1: Foundation & RBAC - Research

## Objective
Answer: "What do I need to know to PLAN this phase well?"

## Existing State
1. **User Model (`backend/app/models/user.py`)**
   - Has a `UserRole` enum with `worker`, `employer`, `govt`, `clinic`.
   - This conflicts with the PRD definitions.
2. **Auth Routes (`backend/app/routes/auth.py`)** 
   - Has `/register` and `/login` endpoints.
   - Issues JWTs containing standard user fields.
3. **Schemas (`backend/app/schemas/auth.py`)**
   - References the old `UserRole` enum.

## What Needs to Change
1. **Model Update**: 
   - `UserRole` enum must be updated to `admin`, `doctor`, `asha_worker`, `migrant_worker`.
   - Database migration will be required if Alembic is used (since enum types in Postgres map to database enums).
2. **RBAC Dependencies**:
   - `backend/app/core/deps.py` or similar should export role requirements, e.g., `def require_role(roles: list[UserRole])`.
   - We need endpoints protected by these dependencies.

## Data Model Impacts
- Existing dummy seeds might break if they rely on the old roles (e.g. `seed_mongodb.py` or `seed.py`). The planner must ensure tests and seeds are updated.

## Output
The plan should instruct the execution agent to:
1. Update `UserRole`.
2. Generate an Alembic migration for the enum change.
3. Create an RBAC dependency in FastApi.
4. Add tests proving that a `doctor` cannot access an `admin` only route, and an `asha_worker` cannot access a `doctor` only route.
