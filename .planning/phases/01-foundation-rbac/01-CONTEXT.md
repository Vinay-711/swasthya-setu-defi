# Phase 1: Foundation & RBAC - Context

**Gathered:** 2026-03-26
**Status:** Ready for planning
**Source:** PRD Express Path (SwasthyaSetu_PRD.md)

<domain>
## Phase Boundary

Establish system roles (Doctor, ASHA, Admin) and standard authentication.
- Must implement Email/Password login for ASHA and Doctor roles.
- Must enforce JWT-based Role-Based Access Control (RBAC) across all endpoints.
- MUST NOT implement OTP login for workers (that is Phase 2).
</domain>

<decisions>
## Implementation Decisions

### Authentication
- Use OAuth2 with Password Flow and JWT tokens (already partially scaffolded in FastAPI).
- Roles: `admin`, `doctor`, `asha_worker`, `migrant_worker`.
- User schema must support email (for Admin/Doctor/ASHA) alongside role mapping.

### Claude's Discretion
- Token expiration times (suggest 60 mins for access, 7 days for refresh).
- Password hashing algorithm (suggest bcrypt via passlib).
- Database table structure for Users if not already fully rigid for these exact roles.
</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Architecture
- `.planning/codebase/ARCHITECTURE.md` — System architecture and FastAPI details.
- `.planning/codebase/STACK.md` — Core technologies in use.
- `.planning/REQUIREMENTS.md` — Source of truth for AUTH-02 and AUTH-03.
</canonical_refs>

<specifics>
## Specific Ideas

- The PRD requires that ASHA workers and Doctors be explicitly invited or created by Admins, rather than open public signup, to ensure trust in the exact personnel handling medical data.
- The system must verify the JWT role on securely scoped endpoints (e.g., `Depends(get_current_active_user)`).
</specifics>

<deferred>
## Deferred Ideas

- OTP/Phone login for migrant workers (deferred to Phase 2).
- ABHA identity linkage (deferred to Phase 3).
</deferred>

---

*Phase: 01-foundation-rbac*
*Context gathered: 2026-03-26 via PRD Express Path*
