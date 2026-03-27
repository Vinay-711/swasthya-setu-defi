const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";
const TOKEN_KEY = "swasthya_token";
const MOCK_MODE_KEY = "swasthya_mock_mode";
const DEFAULT_MOCK_MODE = (import.meta.env.VITE_DEFAULT_MOCK_MODE || "false").toLowerCase() === "true";

const RAMESH_WORKER_ID = "7f0f77a4-8425-4e92-a17f-7cb0f91ef001";

const LOCAL_MOCK = {
  token: {
    access_token: "mock.jwt.token",
    token_type: "bearer",
    user: {
      id: RAMESH_WORKER_ID,
      email: "ramesh.worker@swasthya.in",
      role: "worker",
      swasthya_id: "SW-100001",
      name: "Ramesh Yadav",
      language: "hi",
      age: 34,
      blood_type: "O+",
      allergies: ["dust"],
      current_medications: ["Salbutamol inhaler"],
      recent_diagnoses: ["chronic bronchitis"],
      consent_granted: true,
      created_at: "2026-03-01T09:00:00Z",
    },
  },
  risk: {
    silicosis: 0.87,
    byssinosis: 0.04,
    occupational_asthma: 0.19,
    risk_level: "HIGH",
    predicted_disease: "silicosis",
    top_factors: [
      { feature: "years_in_job", impact: 0.42, value: "8 years" },
      { feature: "task_stone_cutting", impact: 0.31, value: "daily" },
      { feature: "ppe_usage", impact: 0.28, value: "rarely" },
    ],
    recommendations: [
      "Chest X-ray immediately",
      "Spirometry test",
      "Refer to occupational health specialist",
      "Priority follow-up in 72 hours",
    ],
  },
  record: {
    swasthya_id: "SW-100001",
    worker: {
      id: RAMESH_WORKER_ID,
      email: "ramesh.worker@swasthya.in",
      swasthya_id: "SW-100001",
      name: "Ramesh Yadav",
      age: 34,
      blood_type: "O+",
      allergies: ["dust"],
      current_medications: ["Salbutamol inhaler"],
      recent_diagnoses: ["chronic bronchitis"],
      language: "hi",
      state: "Gujarat",
      consent_granted: true,
      created_at: "2026-03-01T09:00:00Z",
    },
    health_records: [
      {
        id: "hr-mock-001",
        worker_id: RAMESH_WORKER_ID,
        record_type: "visit",
        data_json: { summary: "Persistent cough for 6 months" },
        created_at: "2026-03-18T10:45:00Z",
      },
      {
        id: "hr-mock-002",
        worker_id: RAMESH_WORKER_ID,
        record_type: "follow_up",
        data_json: { summary: "Breathlessness while lifting heavy loads" },
        created_at: "2026-03-10T09:00:00Z",
      },
      {
        id: "hr-mock-003",
        worker_id: RAMESH_WORKER_ID,
        record_type: "visit",
        data_json: { summary: "Baseline checkup after migration" },
        created_at: "2026-03-01T08:00:00Z",
      },
    ],
    occupational_risk: [
      {
        id: "risk-mock-001",
        risk_level: "HIGH",
        scores_json: {},
        created_at: "2026-03-18T10:50:00Z",
      },
    ],
    documents: [
      {
        id: "doc-mock-001",
        worker_id: RAMESH_WORKER_ID,
        original_path: "mock://prescriptions/ramesh-visit.png",
        status: "processed",
        parsed_json: {
          medicines: [
            { name: "Salbutamol", dosage: "2mg" },
            { name: "Budesonide", dosage: "200mcg" },
          ],
          diagnosis: ["suspected silicosis"],
        },
        created_at: "2026-03-20T09:30:00Z",
      },
    ],
    notifications: [
      {
        id: "ntf-mock-001",
        worker_id: RAMESH_WORKER_ID,
        channel: "whatsapp",
        message: "High respiratory risk detected. Visit nearest clinic.",
        status: "sent",
        sent_at: "2026-03-18T11:00:00Z",
        created_at: "2026-03-18T11:00:00Z",
      },
    ],
  },
};

function parseJsonSafely(value) {
  if (!value || typeof value !== "string") return {};
  try {
    return JSON.parse(value);
  } catch {
    return {};
  }
}

function normalizeLanguageCode(value) {
  const raw = String(value || "").trim().toLowerCase();
  if (!raw) return null;

  const aliasMap = {
    english: "en",
    hindi: "hi",
    marathi: "mr",
    bengali: "bn",
    tamil: "ta",
    telugu: "te",
    kannada: "kn",
    odia: "or",
    odiya: "or",
    malayalam: "ml",
  };

  if (aliasMap[raw]) return aliasMap[raw];
  if (raw.length <= 3) return raw;
  return raw;
}

function buildMockTranslatedText(text, targetLanguage) {
  const normalized = (targetLanguage || "").toLowerCase();

  if (normalized.startsWith("en")) {
    return "I have chest pain and difficulty breathing.";
  }
  if (normalized.startsWith("hi")) {
    return "मुझे सीने में दर्द हो रहा है और सांस लेने में तकलीफ है।";
  }
  if (normalized.startsWith("mr")) {
    return "मला छातीत वेदना आहे आणि श्वास घेण्यास त्रास होतो आहे.";
  }
  if (normalized.startsWith("bn")) {
    return "আমার বুকে ব্যথা হচ্ছে এবং শ্বাস নিতে কষ্ট হচ্ছে।";
  }
  if (normalized.startsWith("ta")) {
    return "எனக்கு மார்பில் வலி உள்ளது மற்றும் சுவாசிக்க சிரமமாக உள்ளது.";
  }
  if (normalized.startsWith("te")) {
    return "నాకు ఛాతిలో నొప్పి ఉంది మరియు శ్వాస తీసుకోవడంలో ఇబ్బంది ఉంది.";
  }
  if (normalized.startsWith("kn")) {
    return "ನನಗೆ ಎದೆನೋವು ಇದೆ ಮತ್ತು ಉಸಿರಾಟಕ್ಕೆ ತೊಂದರೆ ಆಗುತ್ತಿದೆ.";
  }
  if (normalized.startsWith("or") || normalized.startsWith("od")) {
    return "ମୋର ଛାତିରେ ବେଦନା ହେଉଛି ଏବଂ ଶ୍ୱାସ ନେବାରେ ଅସୁବିଧା ହେଉଛି।";
  }
  if (normalized.startsWith("ml")) {
    return "എനിക്ക് നെഞ്ചുവേദനയുണ്ട്, ശ്വസിക്കാൻ ബുദ്ധിമുട്ടുണ്ട്.";
  }
  return text;
}

export function getToken() {
  return localStorage.getItem(TOKEN_KEY) || "";
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

export function isMockMode() {
  const stored = localStorage.getItem(MOCK_MODE_KEY);
  if (stored === null) {
    return DEFAULT_MOCK_MODE;
  }
  return stored === "true";
}

export function setMockMode(enabled) {
  localStorage.setItem(MOCK_MODE_KEY, enabled ? "true" : "false");
}

function localMockPayload(path, method, options = {}) {
  if (path === "/health" && method === "GET") {
    return { status: "ok", mode: "mock" };
  }

  if (["/auth/register", "/auth/login"].includes(path) && method === "POST") {
    return LOCAL_MOCK.token;
  }

  if (path === "/auth/me" && method === "GET") {
    return LOCAL_MOCK.token.user;
  }

  if (path === "/occupational/risk-profile") {
    return LOCAL_MOCK.risk;
  }

  if (path === "/voice/transcribe" && method === "POST") {
    return {
      text: "mujhe seene mein dard ho raha hai aur sans lene mein takleef hai",
      detected_language: "hi",
    };
  }

  if (path === "/voice/process" && method === "POST") {
    const payload = parseJsonSafely(options.body);
    const text = payload.text || "mujhe seene mein dard ho raha hai aur sans lene mein takleef hai";
    const targetLanguage = normalizeLanguageCode(payload.target_language) || "en";
    return {
      text,
      detected_language: "hi",
      translated_text: buildMockTranslatedText(text, targetLanguage),
      tts_audio_base64: "bW9jay10dHMtYXVkaW8=",
    };
  }

  if (path === "/documents/scan" && method === "POST") {
    return LOCAL_MOCK.record.documents[0];
  }

  if (path.startsWith("/identity/") && path.endsWith("/record") && method === "GET") {
    return LOCAL_MOCK.record;
  }

  if (path.startsWith("/tracking/worker/") && method === "GET") {
    return [
      {
        id: "loc-mock-001",
        worker_id: RAMESH_WORKER_ID,
        state: "Gujarat",
        city: "Surat",
        latitude: "21.1702",
        longitude: "72.8311",
        source: "manual",
        created_at: "2026-03-18T12:00:00Z",
      },
    ];
  }

  return {
    mock: true,
    path,
    method,
    message: "Demo-safe frontend fallback payload",
  };
}

async function request(path, options = {}) {
  const headers = {
    ...(options.headers || {}),
  };

  const token = getToken();
  if (token && !headers.Authorization) {
    headers.Authorization = `Bearer ${token}`;
  }

  const hasBody = options.body !== undefined && options.body !== null;
  if (hasBody && !(options.body instanceof FormData)) {
    headers["Content-Type"] = headers["Content-Type"] || "application/json";
  }

  const method = String(options.method || "GET").toUpperCase();
  const url = new URL(`${API_BASE}${path}`);
  if (isMockMode()) {
    url.searchParams.set("mock", "true");
  }

  try {
    const response = await fetch(url.toString(), {
      ...options,
      headers,
    });

    const contentType = response.headers.get("content-type") || "";
    const payload = contentType.includes("application/json")
      ? await response.json()
      : await response.text();

    if (!response.ok) {
      if (isMockMode()) {
        return localMockPayload(path, method, options);
      }
      const detail = payload?.detail || payload || "Request failed";
      throw new Error(String(detail));
    }

    return payload;
  } catch (error) {
    if (isMockMode()) {
      return localMockPayload(path, method, options);
    }
    throw error;
  }
}

export const api = {
  health: () => request("/health"),
  register: (payload) => request("/auth/register", { method: "POST", body: JSON.stringify(payload) }),
  login: (payload) => request("/auth/login", { method: "POST", body: JSON.stringify(payload) }),
  me: () => request("/auth/me"),
  createIdentity: (userId) => request("/identity/create", { method: "POST", body: JSON.stringify({ user_id: userId }) }),
  getWorkerRecord: (swasthyaId) => request(`/identity/${encodeURIComponent(swasthyaId)}/record`),
  updateConsent: (swasthyaId, consentGranted) =>
    request(`/identity/${encodeURIComponent(swasthyaId)}/consent`, {
      method: "PUT",
      body: JSON.stringify({ consent_granted: consentGranted }),
    }),
  submitRiskProfile: (payload) => request("/occupational/risk-profile", { method: "POST", body: JSON.stringify(payload) }),
  getRiskRecommendations: (workerId) => request(`/occupational/recommendations/${workerId}`),
  uploadDocument: (workerId, file) => {
    const form = new FormData();
    form.append("worker_id", workerId);
    form.append("file", file);
    return request("/documents/scan", { method: "POST", body: form });
  },
  listDocuments: (workerId) => request(`/documents/worker/${workerId}`),
  updateLocation: (payload) => request("/tracking/location", { method: "POST", body: JSON.stringify(payload) }),
  listLocations: (workerId) => request(`/tracking/worker/${workerId}`),
  triggerNotification: (payload) => request("/notifications/trigger", { method: "POST", body: JSON.stringify(payload) }),
  listNotifications: (workerId) => request(`/notifications/worker/${workerId}`),
  transcribeVoice: (fileOrBlob) => {
    const form = new FormData();
    const file =
      fileOrBlob instanceof File
        ? fileOrBlob
        : new File([fileOrBlob], "voice-input.webm", { type: fileOrBlob?.type || "audio/webm" });
    form.append("file", file);
    return request("/voice/transcribe", { method: "POST", body: form });
  },
  processVoice: ({ text, target_language }) =>
    request("/voice/process", {
      method: "POST",
      body: JSON.stringify({ text, target_language: normalizeLanguageCode(target_language) }),
    }),
  voiceTranslate: (payload) =>
    request("/voice/process", {
      method: "POST",
      body: JSON.stringify({
        text: payload?.text || "",
        target_language: normalizeLanguageCode(
          payload?.target_language || payload?.to_lang || payload?.targetLang || payload?.language || null,
        ),
      }),
    }),
};
