# Phase 4 Execution Plan: Health Record MVP

## 1. Schema Updates
- **File:** `app/schemas/health_records.py`
- Add pagination metadata schemas for the response (e.g. `PaginatedHealthRecords`).
- Ensure symptom-specific logic if necessary, or rely on existing `HealthRecordCreate`.

## 2. Service Layer Updates
- **File:** `app/services/health_record_service.py`
- Update `list_worker_health_records` to include `skip: int` and `limit: int` parameters for pagination queries.
- Return both records and a total count for proper pagination UI.

## 3. Route & RBAC Updates
- **File:** `app/routes/health_records.py`
- **CLIN-01**: Update the `GET /worker/{worker_id}` endpoint to accept `skip` and `limit` queries. Add RBAC dependency `require_roles([Role.DOCTOR, Role.ADMIN])` (and allow self-fetching for workers).
- **CLIN-02**: Update the `POST /` creation endpoint to enforce `require_roles([Role.ASHA_WORKER, Role.DOCTOR])` so unauthorized users cannot spam records.

## 4. Tests
- **File:** `tests/test_health_records.py`
- Write comprehensive integration tests simulating:
  - ASHA worker creating a symptom report.
  - Doctor fetching a paginated timeline of worker visits.
  - Proper RBAC rejection for ordinary workers trying to view others' timelines.
