# Domain Research: Stack (Occupational Migrant Health)

## Standard Stack for 2026 Mobile/AI Health
- **Edge Deployment**: Progressive Web Apps (PWA) to avoid Play Store friction and support low-end devices.
- **AI Tooling**: 
  - **Voice**: OpenAI Whisper (fine-tuned for Indic languages) or Bhashini. Essential for low-literacy users.
  - **Vision**: EasyOCR or Tesseract for prescription digitizing.
  - **Predictive ML**: XGBoost/LightGBM for tabular occupational data. Fast, explainable (SHAP), and lightweight compared to deep neural nets.
- **Data Privacy**: PostGIS (for ASHA geospatial routing) and field-level AES-256 encryption. FHIR R4 standard for interoperability.
- **Messaging**: Twilio, Plivo, or Gupshup for WhatsApp/SMS/IVR integrations. IVR is mandatory for zero-literacy segments.

## Why this Stack?
The ecosystem demands offline-capability, low-bandwidth footprint (2G/3G networks), and multi-lingual voice accessibility. Using a heavy framework or requiring huge downloads will kill adoption instantly.
