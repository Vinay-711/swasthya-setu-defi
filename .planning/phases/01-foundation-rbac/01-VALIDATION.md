# Validation Architecture: Phase 1 (Foundation & RBAC)

## Phase Goal
Establish system roles (Doctor, ASHA, Admin) and standard authentication.

## 1. Domain Requirements Validation
- [ ] **AUTH-02**: ASHA worker / Doctor can login via Email and Password. (Verified via unit tests for `/login`).
- [ ] **AUTH-03**: System provisions JWT access tokens with granular role scopes. (Verified by checking JWT claims output in tests).

## 2. Execution Quality Validation
- [ ] All `pytest` tests pass.
- [ ] Alembic migration applied successfully without breaking the DB schema.

## 3. Structural Integrity Validation
- [ ] `UserRole` enum must not contain any legacy values (`worker`, `employer`, etc.).
- [ ] Reused components (`deps.py`) must cleanly abstract the role checking to be easily used by future phases.

## 4. Acceptance Criteria Checklist
- [ ] Admin can create new ASHA worker accounts (via the data model).
- [ ] Doctors can log in securely using Email/Password.
- [ ] API endpoints block unauthorized roles (proven by the admin-only test route).
