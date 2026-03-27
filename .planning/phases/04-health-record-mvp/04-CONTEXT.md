# Phase 4: Health Record MVP Context

## Objective
Enable basic clinical logging for migrant workers, specifically symptom reporting by ASHA workers and timeline viewing by Doctors.

## Requirements
- **CLIN-01**: Doctor can view patient timeline of past visits. This implies fetching a paginated list of health records for a specific worker.
- **CLIN-02**: ASHA worker can log new symptom reports. This implies creating health records with `record_type` representing a symptom report.

## Baseline
A foundational `HealthRecord` model exists with basic CRUD routes in `app/routes/health_records.py`. However, existing endpoints lack:
1. Pagination parameters for scalable timeline views (CLIN-01).
2. Proper Role-Based Access Control (RBAC) to restrict timeline access (Doctors/Admins) and symptom logging (ASHA/Doctors).
