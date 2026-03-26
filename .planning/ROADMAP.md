# Roadmap: SwasthyaSetu

## Overview

SwasthyaSetu will be built in 12 fine-grained phases, starting from foundational access control, building up the core digital health record, injecting intelligence via Domain AI models (Voice, OCR, Risk), and concluding with robust physical-world integrations (Geospatial routing and IVR/SMS notifications).

## Phases

- [ ] **Phase 1: Foundation & RBAC** - Setup roles and static email authentication
- [ ] **Phase 2: Worker OTP Auth** - Mobile OTP authentication for feature phones
- [ ] **Phase 3: Identity & ABHA integration** - QR codes and national ID linkage
- [ ] **Phase 4: Health Record MVP** - CRUD operations for clinical encounters
- [ ] **Phase 5: Document AI** - Image uploads and Prescription OCR
- [ ] **Phase 6: Audio Pipeline MVP** - Whisper integration for audio transcription
- [ ] **Phase 7: BhashaSehat NLP** - IndicBERT semantic parsing of transcripts
- [ ] **Phase 8: KaamSuraksha Schema** - Employment history and XGBoost model scaffolding
- [ ] **Phase 9: Risk Scoring Inference** - Batch/real-time occupational risk scoring
- [ ] **Phase 10: SehatSetu Geo-Routing** - PostGIS integration for ASHA worker assignment
- [ ] **Phase 11: Text Notifications** - Asynchronous SMS/WhatsApp alerts
- [ ] **Phase 12: IVR Fallback Integration** - Voice calls for zero-literacy accessibility

## Phase Details

### Phase 1: Foundation & RBAC
**Goal**: Establish system roles (Doctor, ASHA, Admin) and standard authentication.
**Depends on**: Nothing
**Requirements**: AUTH-02, AUTH-03
**Success Criteria** (what must be TRUE):
  1. Admin can create new ASHA worker accounts.
  2. Doctors can log in securely using Email/Password.
  3. API endpoints block unauthorized roles.
**Plans**: TBD

### Phase 2: Worker OTP Auth
**Goal**: Implement passwordless login for migrant workers.
**Depends on**: Phase 1
**Requirements**: AUTH-01
**Success Criteria** (what must be TRUE):
  1. Worker can request OTP via phone number.
  2. Worker can verify OTP and receive a JWT.
**Plans**: TBD

### Phase 3: Identity & ABHA integration
**Goal**: Create portable health IDs.
**Depends on**: Phase 2
**Requirements**: ID-01, ID-02
**Success Criteria** (what must be TRUE):
  1. System generates a unique QR code for each worker profile.
  2. Account can be linked to an existing ABHA number.
**Plans**: TBD

### Phase 4: Health Record MVP
**Goal**: Enable basic clinical logging.
**Depends on**: Phase 3
**Requirements**: CLIN-01, CLIN-02
**Success Criteria** (what must be TRUE):
  1. ASHA worker can submit a text-based symptom report for a worker.
  2. Doctor can fetch a paginated timeline of worker visits.
**Plans**: TBD

### Phase 5: Document AI
**Goal**: Digitize paper records automatically.
**Depends on**: Phase 4
**Requirements**: CLIN-03
**Success Criteria** (what must be TRUE):
  1. API accepts image uploads.
  2. OCR extracts readable text from standard prescription images.
**Plans**: TBD

### Phase 6: Audio Pipeline MVP
**Goal**: Transcribe voice notes securely.
**Depends on**: Phase 4
**Requirements**: VOIC-01, VOIC-02
**Success Criteria** (what must be TRUE):
  1. Client can submit an audio file blob.
  2. Whisper model returns accurate text transcript in Hindi/Regional language.
**Plans**: TBD

### Phase 7: BhashaSehat NLP
**Goal**: Extract clinical intent from transcribed text.
**Depends on**: Phase 6
**Requirements**: VOIC-03
**Success Criteria** (what must be TRUE):
  1. NLP model classifies transcript text into medical symptoms/intents.
**Plans**: TBD

### Phase 8: KaamSuraksha Schema
**Goal**: Track occupational history for predictive modeling.
**Depends on**: Phase 4
**Requirements**: RISK-01, RISK-02
**Success Criteria** (what must be TRUE):
  1. Worker profile supports chronological employment history array.
  2. XGBoost model binary is loaded and accessible via the predictor service.
**Plans**: TBD

### Phase 9: Risk Scoring Inference
**Goal**: Operationalize disease prediction.
**Depends on**: Phase 8
**Requirements**: RISK-03
**Success Criteria** (what must be TRUE):
  1. Adding a high-risk occupation (e.g., Coal mining) triggers a risk recalculation.
  2. ASHA dashboard visually flags workers with a risk score > 0.8.
**Plans**: TBD

### Phase 10: SehatSetu Geo-Routing
**Goal**: Maintain care continuity when migrants move.
**Depends on**: Phase 9
**Requirements**: CARE-01
**Success Criteria** (what must be TRUE):
  1. System stores geospatial coordinates of clinics and active projects.
  2. Updating a worker's primary location reassigns them to the nearest ASHA user.
**Plans**: TBD

### Phase 11: Text Notifications
**Goal**: Enable reliable asynchronous messaging.
**Depends on**: Phase 1
**Requirements**: NOTF-01
**Success Criteria** (what must be TRUE):
  1. System queues Celery tasks for notifications.
  2. Worker receives SMS when an appointment is scheduled.
**Plans**: TBD

### Phase 12: IVR Fallback Integration
**Goal**: Reach illiterate workers without smartphones.
**Depends on**: Phase 11
**Requirements**: NOTF-02
**Success Criteria** (what must be TRUE):
  1. If SMS delivery fails or user preference is Voice, system triggers an automated phone call.
**Plans**: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → ... → 12

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation & RBAC | 0/TBD | Not started | - |
| 2. Worker OTP Auth | 0/TBD | Not started | - |
| 3. Identity & ABHA integration | 0/TBD | Not started | - |
| 4. Health Record MVP | 0/TBD | Not started | - |
| 5. Document AI | 0/TBD | Not started | - |
| 6. Audio Pipeline MVP | 0/TBD | Not started | - |
| 7. BhashaSehat NLP | 0/TBD | Not started | - |
| 8. KaamSuraksha Schema | 0/TBD | Not started | - |
| 9. Risk Scoring Inference | 0/TBD | Not started | - |
| 10. SehatSetu Geo-Routing | 0/TBD | Not started | - |
| 11. Text Notifications | 0/TBD | Not started | - |
| 12. IVR Fallback Integration | 0/TBD | Not started | - |
