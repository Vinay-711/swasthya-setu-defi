# Requirements: SwasthyaSetu

**Defined:** 2026-03-26
**Core Value:** Ensure no migrant worker loses healthcare access or goes undiagnosed for occupational diseases due to geography, language, or lack of records.

## v1 Requirements

### Authentication & Identity
- [ ] **AUTH-01**: Worker can login via phone number OTP (no password required).
- [ ] **AUTH-02**: ASHA worker / Doctor can login via Email and Password.
- [ ] **AUTH-03**: System provisions JWT access tokens with granular role scopes.
- [ ] **ID-01**: Generate SwasthyaID QR code for workers.
- [ ] **ID-02**: Integrate with ABDM to link SwasthyaID with ABHA number.

### Clinical Records
- [ ] **CLIN-01**: Doctor can view patient timeline of past visits.
- [ ] **CLIN-02**: ASHA worker can log new symptom reports.
- [ ] **CLIN-03**: System can extract structured text from uploaded prescription images using OCR.

### Voice & Language (BhashaSehat)
- [ ] **VOIC-01**: System accepts raw audio file uploads from the mobile client.
- [ ] **VOIC-02**: Audio is transcribed accurately using Whisper (Indic dialects).
- [ ] **VOIC-03**: Transcripts are parsed for medical intents using IndicBERT.

### Occupational AI (KaamSuraksha)
- [ ] **RISK-01**: Workers' job history is logged with industry-standard occupational codes.
- [ ] **RISK-02**: XGBoost model inferences risk scores for respiratory/musculoskeletal diseases.
- [ ] **RISK-03**: High-risk workers are automatically flagged in the ASHA dashboard.

### Care Continuity (SehatSetu) & Notifications
- [ ] **CARE-01**: Worker's location change triggers re-assignment to nearest local ASHA worker (Geospatial).
- [ ] **NOTF-01**: Critical alerts are routed via WhatsApp or SMS.
- [ ] **NOTF-02**: If SMS fails or user is illiterate, system falls back to IVR phone call.

## v2 Requirements

### Analytics & Reporting
- **STAT-01**: Government dashboard for macro-level migration health trends.
- **STAT-02**: Predictive supply chain alerts for medicine shortages at local clinics.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Automated Diagnosis | AI is for screening/flagging only. Doctors must make actual diagnoses. |
| Smartphone App Only | Imposes hardware barrier on poorest 30% of migrants. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| AUTH-01 | Phase 2 | Pending |
| AUTH-02 | Phase 1 | Pending |
| AUTH-03 | Phase 1 | Pending |
| ID-01 | Phase 3 | Pending |
| ID-02 | Phase 3 | Pending |
| CLIN-01 | Phase 4 | Pending |
| CLIN-02 | Phase 4 | Pending |
| CLIN-03 | Phase 5 | Pending |
| VOIC-01 | Phase 6 | Pending |
| VOIC-02 | Phase 6 | Pending |
| VOIC-03 | Phase 7 | Pending |
| RISK-01 | Phase 8 | Pending |
| RISK-02 | Phase 8 | Pending |
| RISK-03 | Phase 9 | Pending |
| CARE-01 | Phase 10 | Pending |
| NOTF-01 | Phase 11 | Pending |
| NOTF-02 | Phase 12 | Pending |

**Coverage:**
- v1 requirements: 17 total
- Mapped to phases: 17
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-26*
