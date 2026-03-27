---
wave: 1
depends_on: []
files_modified: ["backend/app/models/user.py", "backend/app/schemas/identity.py", "backend/app/routes/identity.py", "backend/app/services/identity_service.py", "backend/tests/test_identity.py"]
autonomous: true
---

# 01-PLAN: ABHA Integration

## Requirements
ID-02

## Goal
Add `abha_number` string column to User model, `LinkABHARequest` to schemas, implement `POST /identity/{swasthya_id}/link-abha` endpoint, and create API endpoints testing logic.

## Tasks

<task>
<read_first>
- backend/app/models/user.py
</read_first>
<action>
1. Add `abha_number: Mapped[str | None] = mapped_column(String(14), unique=True, nullable=True, index=True)` to the `User` class.
</action>
<acceptance_criteria>
`grep "abha_number.*Mapped\[str" backend/app/models/user.py` exits 0.
</acceptance_criteria>
</task>

<task>
<read_first>
- backend/app/schemas/identity.py
</read_first>
<action>
1. Add `abha_number: str | None` to the `WorkerClinicProfile` class.
2. Create a new schema class `LinkABHARequest(BaseModel)` containing `abha_number: str`.
</action>
<acceptance_criteria>
`grep "LinkABHARequest" backend/app/schemas/identity.py` exits 0.
</acceptance_criteria>
</task>

<task>
<read_first>
- backend/app/services/identity_service.py
</read_first>
<action>
1. Add function `link_worker_abha(db: AsyncSession, swasthya_id: str, abha_number: str) -> User | None:` to update and successfully link ABHA number for a worker. The function uses `get_worker_by_swasthya_id` then updates `worker.abha_number = abha_number` and handles `db.commit()` and `db.refresh()`.
</action>
<acceptance_criteria>
`grep "def link_worker_abha" backend/app/services/identity_service.py` exits 0.
</acceptance_criteria>
</task>

<task>
<read_first>
- backend/app/routes/identity.py
</read_first>
<action>
1. Import `LinkABHARequest` from schemas and `link_worker_abha` from services.
2. Add `@router.post("/{swasthya_id}/link-abha")` to link an ABHA. Endpoint function `link_abha(swasthya_id: str, payload: LinkABHARequest, db=Depends(...))`
3. Endpoint should return `{"swasthya_id": ..., "abha_number": ...}`.
</action>
<acceptance_criteria>
`grep "@router.post.*link-abha" backend/app/routes/identity.py` exits 0.
</acceptance_criteria>
</task>

<task>
<read_first>
- backend/tests/test_otp.py
</read_first>
<action>
1. Create `backend/tests/test_identity.py`.
2. Write integration tests to check linking ABHA number works (using a mock user / mocked swasthya_id).
</action>
<acceptance_criteria>
`pytest backend/tests/test_identity.py` exits 0.
</acceptance_criteria>
</task>
