# Phase 3: Identity & ABHA integration - Context

**Gathered:** 2026-03-26
**Status:** Ready for planning
**Source:** Autonomous completion

<domain>
## Phase Boundary
Create portable health IDs for migrant workers.
- System generates a unique QR code for each worker profile.
- Account can be linked to an existing ABHA (Ayushman Bharat Health Account) number.
</domain>

<decisions>
## Implementation Decisions

### ID-01: Generate SwasthyaID QR code for workers
- **QR Code Generation**: Add an endpoint `GET /users/{phone}/qr` that returns a QR code image (PNG) or base64 string encoding the worker's unique identifier (e.g., UUID or phone_hash).
- **Library**: Use a standard Python QR code library (e.g., `qrcode`).
- **Data Encoded**: The QR code should encode a JSON payload or a URI that uniquely identifies the worker securely (e.g., `{"id": "user-uuid"}`).

### ID-02: Integrate with ABDM to link SwasthyaID with ABHA number
- **ABHA Linking**: Add a new column `abha_number` (String, unique, nullable) to the `User` model.
- **Endpoint**: Implement `POST /users/link-abha` which accepts the `abha_number` and associates it with the currently authenticated worker.
- **Validation**: Ensure basic format validation for the ABHA number (e.g., 14-digit format).

### Claude's Discretion
- Database schema migration tools (Alembic) to add the `abha_number` column.
- Security of the QR code endpoint (should require appropriate JWT auth or be suitably scoped).
</decisions>

<canonical_refs>
## Canonical References
No external specs — requirements fully captured in decisions above.
</canonical_refs>

<specifics>
## Specific Ideas
- Generate the QR code dynamically rather than storing the image in the database.
- Return the QR code as a `StreamingResponse` or base64 encoded string depending on standard best practices.
</specifics>

<deferred>
## Deferred Ideas
- Deep integration with the ABDM API for actual ABHA creation or OTP verification (defer to a later phase if necessary, or just mock the ABHA linking for now).
</deferred>
