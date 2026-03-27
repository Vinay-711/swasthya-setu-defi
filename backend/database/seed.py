# pyre-ignore-all-errors
"""
Comprehensive seed script for SwasthyaSetu demo.
Populates: 15 workers across 8 occupations, 1 employer, 3 ASHA workers, 1 doctor.
All linked by IDs with realistic medical histories matching India's
migrant-worker health landscape (ICMR / NIOH research-based).
"""
import asyncio
from datetime import datetime, timedelta, timezone

from sqlalchemy import select  # pyre-ignore[21]

from app.core.security import hash_password  # pyre-ignore[21]
from app.models.health_record import HealthRecord  # pyre-ignore[21]
from app.models.location_log import LocationLog  # pyre-ignore[21]
from app.models.notification import Notification  # pyre-ignore[21]
from app.models.risk_profile import RiskProfile  # pyre-ignore[21]
from app.models.user import User, UserRole  # pyre-ignore[21]
from database.init_db import init_db  # pyre-ignore[21]
from database.session import SessionLocal  # pyre-ignore[21]
from app.utils.crypto import encrypt_text, get_phone_hash  # pyre-ignore[21]

# ---------------------------------------------------------------------------
# Fixed UUIDs — deterministic, cross-linkable
# ---------------------------------------------------------------------------
W = {  # 15 workers
    "ramesh":   "a1000001-0001-4000-8000-000000000001",
    "suresh":   "a1000001-0002-4000-8000-000000000002",
    "meena":    "a1000001-0003-4000-8000-000000000003",
    "dinesh":   "a1000001-0004-4000-8000-000000000004",
    "lakshman": "a1000001-0005-4000-8000-000000000005",
    "parvati":  "a1000001-0006-4000-8000-000000000006",
    "gopal":    "a1000001-0007-4000-8000-000000000007",
    "sunita":   "a1000001-0008-4000-8000-000000000008",
    "mohan":    "a1000001-0009-4000-8000-000000000009",
    "savitri":  "a1000001-0010-4000-8000-000000000010",
    "raju":     "a1000001-0011-4000-8000-000000000011",
    "kamla":    "a1000001-0012-4000-8000-000000000012",
    "bharat":   "a1000001-0013-4000-8000-000000000013",
    "geeta":    "a1000001-0014-4000-8000-000000000014",
    "shankar":  "a1000001-0015-4000-8000-000000000015",
}
EMPLOYER_ID = "b2000001-0001-4000-8000-000000000010"
ASHA_IDS = {
    "priya":   "c3000001-0001-4000-8000-000000000021",
    "lakshmi": "c3000001-0002-4000-8000-000000000022",
    "anita":   "c3000001-0003-4000-8000-000000000023",
}
DOCTOR_ID = "d4000001-0001-4000-8000-000000000031"

NOW = datetime.now(timezone.utc)
DEFAULT_PWD = hash_password("Demo@2025")


def _phone(number: str):
    return encrypt_text(number), get_phone_hash(number)


# Worker profile definitions (demographics based on NSSO / CMS survey data)
WORKERS: list[dict] = [  # type: ignore[type-arg]
    # ── Stone Quarry / Construction (HIGH risk) ──
    {"key": "ramesh", "email": "ramesh.k@swasthya.in", "name": "Ramesh Kumar",
     "phone": "9876500001", "age": 34, "blood": "B+", "lang": "or", "state": "Odisha",
     "sw_id": "SW-100001", "abha": "91100010000001",
     "allergies": ["dust","cement"], "meds": ["Metformin 500mg","Amlodipine 5mg"],
     "diagnoses": ["Type-2 Diabetes","Hypertension Stage 1"]},
    {"key": "dinesh", "email": "dinesh.b@swasthya.in", "name": "Dinesh Barik",
     "phone": "9876500004", "age": 42, "blood": "O-", "lang": "or", "state": "Odisha",
     "sw_id": "SW-100004", "abha": "91100010000004",
     "allergies": ["silica dust"], "meds": ["Pirfenidone 200mg"],
     "diagnoses": ["Silicosis Stage II","Chronic Bronchitis"]},
    {"key": "shankar", "email": "shankar.m@swasthya.in", "name": "Shankar Mahto",
     "phone": "9876500015", "age": 38, "blood": "A+", "lang": "hi", "state": "Jharkhand",
     "sw_id": "SW-100015", "abha": "91100010000015",
     "allergies": ["cement dust"], "meds": ["Salbutamol Inhaler","Montelukast 10mg"],
     "diagnoses": ["Occupational Asthma","Acid Reflux"]},

    # ── Construction (rebar/scaffolding) ──
    {"key": "suresh", "email": "suresh.p@swasthya.in", "name": "Suresh Pradhan",
     "phone": "9876500002", "age": 28, "blood": "O+", "lang": "hi", "state": "Jharkhand",
     "sw_id": "SW-100002", "abha": "91100010000002",
     "allergies": ["penicillin"], "meds": ["Salbutamol Inhaler"],
     "diagnoses": ["Occupational Asthma","Chronic Back Pain"]},
    {"key": "raju", "email": "raju.s@swasthya.in", "name": "Raju Singh",
     "phone": "9876500011", "age": 31, "blood": "B+", "lang": "hi", "state": "UP",
     "sw_id": "SW-100011", "abha": "91100010000011",
     "allergies": [], "meds": ["Diclofenac Gel"],
     "diagnoses": ["Lumbar Disc Herniation"]},

    # ── Textile Mill (Byssinosis risk) ──
    {"key": "parvati", "email": "parvati.n@swasthya.in", "name": "Parvati Nayak",
     "phone": "9876500006", "age": 29, "blood": "A+", "lang": "or", "state": "Odisha",
     "sw_id": "SW-100006", "abha": "91100010000006",
     "allergies": ["cotton dust"], "meds": ["Beclometasone Inhaler"],
     "diagnoses": ["Byssinosis Grade 1","Monday Fever Syndrome"]},
    {"key": "kamla", "email": "kamla.d@swasthya.in", "name": "Kamla Devi",
     "phone": "9876500012", "age": 35, "blood": "AB+", "lang": "hi", "state": "Rajasthan",
     "sw_id": "SW-100012", "abha": "91100010000012",
     "allergies": ["jute fiber"], "meds": ["Theophylline 200mg"],
     "diagnoses": ["Chronic Obstructive Airway Disease"]},

    # ── Mining (CWP risk) ──
    {"key": "gopal", "email": "gopal.k@swasthya.in", "name": "Gopal Kerketta",
     "phone": "9876500007", "age": 45, "blood": "O+", "lang": "hi", "state": "Chhattisgarh",
     "sw_id": "SW-100007", "abha": "91100010000007",
     "allergies": ["coal dust"], "meds": ["Prednisolone 5mg","Doxycycline"],
     "diagnoses": ["Coal Workers Pneumoconiosis","Chronic Bronchitis"]},
    {"key": "bharat", "email": "bharat.o@swasthya.in", "name": "Bharat Oraon",
     "phone": "9876500013", "age": 40, "blood": "A-", "lang": "hi", "state": "Jharkhand",
     "sw_id": "SW-100013", "abha": "91100010000013",
     "allergies": [], "meds": ["Salbutamol PRN"],
     "diagnoses": ["Noise-Induced Hearing Loss","Chronic Cough"]},

    # ── Chemical Factory ──
    {"key": "mohan", "email": "mohan.r@swasthya.in", "name": "Mohan Ram",
     "phone": "9876500009", "age": 33, "blood": "B-", "lang": "hi", "state": "UP",
     "sw_id": "SW-100009", "abha": "91100010000009",
     "allergies": ["isocyanates","latex"], "meds": ["Cetirizine 10mg","Dermatology cream"],
     "diagnoses": ["Chemical Dermatitis","Allergic Rhinitis"]},

    # ── Brick Kiln ──
    {"key": "lakshman", "email": "lakshman.s@swasthya.in", "name": "Lakshman Sahu",
     "phone": "9876500005", "age": 36, "blood": "A-", "lang": "or", "state": "Odisha",
     "sw_id": "SW-100005", "abha": "91100010000005",
     "allergies": [], "meds": ["ORS packets"],
     "diagnoses": ["Recurrent Heat Exhaustion","Chronic Low-Back Pain"]},

    # ── Agriculture / Domestic ──
    {"key": "meena", "email": "meena.d@swasthya.in", "name": "Meena Devi",
     "phone": "9876500003", "age": 26, "blood": "A+", "lang": "or", "state": "Odisha",
     "sw_id": "SW-100003", "abha": "91100010000003",
     "allergies": [], "meds": ["Iron + Folic Acid","Calcium"],
     "diagnoses": ["Iron-Deficiency Anemia","Vitamin D Deficiency"]},
    {"key": "sunita", "email": "sunita.t@swasthya.in", "name": "Sunita Tudu",
     "phone": "9876500008", "age": 24, "blood": "O+", "lang": "sat", "state": "West Bengal",
     "sw_id": "SW-100008", "abha": "91100010000008",
     "allergies": ["pesticides"], "meds": ["Chlorpheniramine"],
     "diagnoses": ["Organophosphate Exposure","Skin Rash"]},
    {"key": "savitri", "email": "savitri.m@swasthya.in", "name": "Savitri Munda",
     "phone": "9876500010", "age": 22, "blood": "B+", "lang": "hi", "state": "Chhattisgarh",
     "sw_id": "SW-100010", "abha": "91100010000010",
     "allergies": [], "meds": [],
     "diagnoses": ["Underweight (BMI 16.8)","Vitamin B12 Deficiency"]},
    {"key": "geeta", "email": "geeta.p@swasthya.in", "name": "Geeta Patel",
     "phone": "9876500014", "age": 30, "blood": "A+", "lang": "gu", "state": "Rajasthan",
     "sw_id": "SW-100014", "abha": "91100010000014",
     "allergies": ["NSAIDs"], "meds": ["Pantoprazole 40mg"],
     "diagnoses": ["Gastritis","Chronic Fatigue"]},
]

# Occupational risk profiles — scores calibrated to real data from NIOH Ahmedabad
RISK_DATA = {
    "ramesh":   ("construction_mason",   ["brick_laying","cement_mixing","scaffolding"],
                 ["persistent_cough","skin_irritation","frequent_urination"],
                 12, {"silicosis":0.65,"dermatitis":0.72,"diabetes_complication":0.81}, "HIGH"),
    "dinesh":   ("stone_quarry",         ["drilling","stone_cutting","blasting"],
                 ["persistent_cough","breathlessness","chest_tightness"],
                 18, {"silicosis":0.91,"lung_fibrosis":0.85,"cor_pulmonale":0.42}, "HIGH"),
    "shankar":  ("stone_quarry",         ["drilling","crushing","loading"],
                 ["wheezing","cough_after_work","chest_pain"],
                 14, {"silicosis":0.78,"occupational_asthma":0.82,"gerd":0.35}, "HIGH"),
    "suresh":   ("construction_rebar",   ["rebar_tying","welding","heavy_lifting"],
                 ["wheezing","back_pain","cough_after_work"],
                 6,  {"respiratory":0.74,"musculoskeletal":0.68,"injury_recurrence":0.55}, "MEDIUM"),
    "raju":     ("scaffolding",          ["scaffolding","heavy_lifting","height_work"],
                 ["back_pain","vertigo"],
                 7,  {"fall_risk":0.72,"musculoskeletal":0.78,"heat_stress":0.45}, "MEDIUM"),
    "parvati":  ("textile_mill_worker",  ["spinning","weaving","carding"],
                 ["chest_tightness","monday_cough","breathlessness"],
                 8,  {"byssinosis":0.81,"occupational_asthma":0.65,"hearing_loss":0.32}, "HIGH"),
    "kamla":    ("textile_mill_worker",  ["weaving","dyeing","chemical_finishing"],
                 ["persistent_cough","skin_rash"],
                 11, {"byssinosis":0.72,"chemical_dermatitis":0.58,"copd":0.65}, "HIGH"),
    "gopal":    ("coal_mining",          ["underground_mining","drilling","hauling"],
                 ["persistent_cough","breathlessness","sputum_black"],
                 20, {"cwp":0.88,"silicosis":0.75,"chronic_bronchitis":0.82}, "HIGH"),
    "bharat":   ("mining",               ["surface_mining","explosives","transport"],
                 ["hearing_loss","cough","fatigue"],
                 15, {"nihl":0.78,"silicosis":0.62,"vibration_syndrome":0.45}, "MEDIUM"),
    "mohan":    ("chemical_factory",     ["chemical_mixing","solvent_handling","cleaning"],
                 ["skin_rash","burning_eyes","headache"],
                 9,  {"chemical_dermatitis":0.82,"respiratory_sensitization":0.71,"liver_risk":0.38}, "HIGH"),
    "lakshman": ("brick_kiln",           ["clay_molding","kiln_firing","brick_carrying"],
                 ["heat_exhaustion","back_pain","dehydration"],
                 10, {"heat_stroke":0.75,"musculoskeletal":0.72,"skin_burns":0.48}, "MEDIUM"),
    "meena":    ("domestic_worker",      ["cleaning","cooking","childcare"],
                 ["fatigue","dizziness","body_ache"],
                 4,  {"anemia_severity":0.58,"nutritional_risk":0.62,"pregnancy_risk":0.40}, "MEDIUM"),
    "sunita":   ("agriculture",          ["spraying","harvesting","manual_weeding"],
                 ["skin_rash","nausea","dizziness"],
                 5,  {"pesticide_poisoning":0.72,"skin_disease":0.65,"respiratory":0.38}, "MEDIUM"),
    "savitri":  ("domestic_worker",      ["cleaning","cooking"],
                 ["fatigue","weakness"],
                 2,  {"nutritional_risk":0.82,"anemia_severity":0.55}, "MEDIUM"),
    "geeta":    ("agriculture",          ["harvesting","grain_processing"],
                 ["abdominal_pain","fatigue"],
                 8,  {"musculoskeletal":0.55,"gastric_risk":0.68,"nutritional":0.42}, "LOW"),
}

# Migration routes (source → destination)
LOCATIONS = {
    "ramesh":   [("Odisha","Berhampur","19.3150","84.7941"), ("Karnataka","Bengaluru","12.9716","77.5946")],
    "suresh":   [("Jharkhand","Ranchi","23.3441","85.3096"), ("Karnataka","Bengaluru","12.9352","77.6245")],
    "meena":    [("Odisha","Bhawanipatna","19.9072","83.1684"), ("Karnataka","Bengaluru","12.9141","77.6411")],
    "dinesh":   [("Odisha","Balangir","20.7200","83.4888"), ("Gujarat","Ahmedabad","23.0225","72.5714")],
    "lakshman": [("Odisha","Nuapada","20.8200","82.5500"), ("Maharashtra","Pune","18.5204","73.8567")],
    "parvati":  [("Odisha","Ganjam","19.5850","84.9800"), ("Gujarat","Surat","21.1702","72.8311")],
    "gopal":    [("Chhattisgarh","Korba","22.3595","82.7501"), ("Maharashtra","Nagpur","21.1458","79.0882")],
    "sunita":   [("West Bengal","Purulia","23.3320","86.3650"), ("Karnataka","Bengaluru","13.0230","77.6500")],
    "mohan":    [("UP","Gorakhpur","26.7606","83.3732"), ("Gujarat","Vapi","20.3714","72.9047")],
    "savitri":  [("Chhattisgarh","Jashpur","22.8850","84.1400"), ("Maharashtra","Mumbai","19.0760","72.8777")],
    "raju":     [("UP","Azamgarh","26.0735","83.1850"), ("Karnataka","Bengaluru","12.9800","77.5900")],
    "kamla":    [("Rajasthan","Bhilwara","25.3470","74.6350"), ("Gujarat","Surat","21.1800","72.8200")],
    "bharat":   [("Jharkhand","Hazaribagh","23.9925","85.3637"), ("Maharashtra","Chandrapur","19.9615","79.2961")],
    "geeta":    [("Rajasthan","Pali","25.7711","73.3234"), ("Gujarat","Ahmedabad","23.0300","72.5800")],
    "shankar":  [("Jharkhand","Giridih","24.1850","86.3010"), ("Karnataka","Bengaluru","13.0100","77.5700")],
}


async def seed() -> None:
    await init_db()
    async with SessionLocal() as db:
        # ── Idempotency check ──
        exists = (await db.execute(
            select(User).where(User.id == W["ramesh"])
        )).scalar_one_or_none()
        if exists:
            print("✔ Seed data already present — skipping.")
            return

        # ================================================================
        #  1. MIGRANT WORKERS (15)
        # ================================================================
        worker_objs: dict[str, User] = {}
        for wd in WORKERS:
            ph = _phone(wd["phone"])
            u = User(
                id=W[wd["key"]], email=wd["email"], hashed_password=DEFAULT_PWD,
                role=UserRole.migrant_worker, name=wd["name"],
                phone_encrypted=ph[0], phone_hash=ph[1],
                age=wd["age"], blood_type=wd["blood"],
                allergies=wd["allergies"],
                current_medications=wd["meds"],
                recent_diagnoses=wd["diagnoses"],
                language=wd["lang"], state=wd["state"],
                swasthya_id=wd["sw_id"], abha_number=wd["abha"],
            )
            worker_objs[wd["key"]] = u
        db.add_all(list(worker_objs.values()))
        await db.flush()

        # ================================================================
        #  2. EMPLOYER
        # ================================================================
        phone_emp = _phone("9800000010")
        employer = User(
            id=EMPLOYER_ID, email="hr@blrbuild.co.in", hashed_password=DEFAULT_PWD,
            role=UserRole.admin, name="Bengaluru BuildCon Pvt Ltd",
            phone_encrypted=phone_emp[0], phone_hash=phone_emp[1],
            allergies=[], current_medications=[], recent_diagnoses=[],
            language="en", state="Karnataka", swasthya_id="SW-EMP-001",
        )
        db.add(employer)

        # ================================================================
        #  3. ASHA WORKERS (3)
        # ================================================================
        for key, aid in ASHA_IDS.items():
            ad = {"priya":   ("priya.asha@swasthya.in","Priya Sahu","9800000021","Odisha","or","SW-ASHA-001"),
                  "lakshmi": ("lakshmi.asha@swasthya.in","Lakshmi Nayak","9800000022","Odisha","or","SW-ASHA-002"),
                  "anita":   ("anita.asha@swasthya.in","Anita Behera","9800000023","Karnataka","kn","SW-ASHA-003")}[key]
            ph = _phone(ad[2])
            db.add(User(id=aid, email=ad[0], hashed_password=DEFAULT_PWD,
                        role=UserRole.asha_worker, name=ad[1],
                        phone_encrypted=ph[0], phone_hash=ph[1],
                        language=ad[4], state=ad[3], swasthya_id=ad[5],
                        allergies=[], current_medications=[], recent_diagnoses=[]))

        # ================================================================
        #  4. DOCTOR
        # ================================================================
        phone_doc = _phone("9800000031")
        doctor = User(
            id=DOCTOR_ID, email="dr.kavitha@swasthya.in", hashed_password=DEFAULT_PWD,
            role=UserRole.doctor, name="Dr. Kavitha Rao",
            phone_encrypted=phone_doc[0], phone_hash=phone_doc[1],
            age=42, blood_type="AB+",
            allergies=[], current_medications=[], recent_diagnoses=[],
            language="kn", state="Karnataka", swasthya_id="SW-DOC-001",
        )
        db.add(doctor)
        await db.flush()

        # ================================================================
        #  5. HEALTH RECORDS — Realistic, diverse medical histories
        # ================================================================
        HR = HealthRecord
        health_records = [
            # Ramesh — Diabetic + Construction worker
            HR(worker_id=W["ramesh"], record_type="visit", data_json={
                "date":(NOW-timedelta(days=180)).isoformat(),
                "facility":"Ganjam District Hospital, Odisha","doctor":"Dr. S. Mishra",
                "chief_complaint":"Frequent urination, increased thirst",
                "diagnosis":"Type-2 Diabetes Mellitus",
                "vitals":{"bp":"148/92","sugar_fasting":186,"hba1c":7.8,"weight_kg":72},
                "prescription":["Metformin 500mg BD","Amlodipine 5mg OD"]}),
            HR(worker_id=W["ramesh"], record_type="lab", data_json={
                "date":(NOW-timedelta(days=45)).isoformat(),
                "facility":"PHC Ramanagara, Karnataka",
                "tests":{"fasting_glucose":{"value":152,"unit":"mg/dL"},
                         "hba1c":{"value":7.2,"unit":"%"},"creatinine":{"value":1.1,"unit":"mg/dL"}}}),
            HR(worker_id=W["ramesh"], record_type="screening", data_json={
                "date":(NOW-timedelta(days=30)).isoformat(),
                "type":"Occupational Health Screening",
                "facility":"Mobile Camp — BuildCon Site #4",
                "results":{"lung_function":"FEV1 82% — mild restriction",
                           "skin_check":"Contact dermatitis — cement","hearing":"Normal"}}),
            # Suresh — Asthma + Back pain
            HR(worker_id=W["suresh"], record_type="visit", data_json={
                "date":(NOW-timedelta(days=120)).isoformat(),
                "facility":"Ranchi Sadar Hospital, Jharkhand","doctor":"Dr. A. Oraon",
                "diagnosis":"Occupational Asthma, Lumbar spondylosis",
                "vitals":{"bp":"124/80","spo2":96,"weight_kg":65},
                "prescription":["Salbutamol Inhaler PRN","Diclofenac Gel topical"]}),
            HR(worker_id=W["suresh"], record_type="injury", data_json={
                "date":(NOW-timedelta(days=60)).isoformat(),
                "facility":"PHC Bengaluru East","type":"Workplace Injury",
                "description":"Laceration on left forearm from rebars",
                "treatment":"4 sutures, TT booster","days_off":3}),
            # Meena — Anemia + Pregnancy
            HR(worker_id=W["meena"], record_type="visit", data_json={
                "date":(NOW-timedelta(days=90)).isoformat(),
                "facility":"Kalahandi DH, Odisha","doctor":"Dr. P. Jena",
                "diagnosis":"Iron-Deficiency Anemia (Hb 8.2 g/dL)",
                "vitals":{"bp":"110/70","hr":92,"weight_kg":48},
                "prescription":["Ferrous Sulphate 200mg OD","Folic Acid 5mg","Calcium + VitD3"]}),
            HR(worker_id=W["meena"], record_type="anc", data_json={
                "date":(NOW-timedelta(days=15)).isoformat(),
                "type":"ANC-2","gestational_weeks":20,
                "facility":"Urban PHC, Bengaluru South",
                "vitals":{"bp":"116/74","weight_kg":51},
                "tests":{"hemoglobin":{"value":10.1,"status":"Improving"}}}),
            # Dinesh — Advanced silicosis
            HR(worker_id=W["dinesh"], record_type="visit", data_json={
                "date":(NOW-timedelta(days=200)).isoformat(),
                "facility":"NIOH Ahmedabad","doctor":"Dr. R. Shah",
                "diagnosis":"Silicosis Stage II — bilateral nodular opacities",
                "vitals":{"bp":"132/86","spo2":91,"fev1":"58%","fvc":"72%"},
                "prescription":["Pirfenidone 200mg TID","Supplemental O2 PRN"]}),
            HR(worker_id=W["dinesh"], record_type="imaging", data_json={
                "date":(NOW-timedelta(days=195)).isoformat(),
                "type":"HRCT Chest","facility":"NIOH Ahmedabad",
                "findings":"Multiple nodules 3-10mm in upper zones, eggshell calcification of hilar nodes",
                "impression":"Progressive massive fibrosis — silicosis Stage II"}),
            # Parvati — Textile byssinosis
            HR(worker_id=W["parvati"], record_type="visit", data_json={
                "date":(NOW-timedelta(days=70)).isoformat(),
                "facility":"Civil Hospital, Surat","doctor":"Dr. M. Patel",
                "diagnosis":"Byssinosis Grade 1 — Monday morning tightness",
                "vitals":{"bp":"118/76","spo2":95},
                "prescription":["Beclometasone Inhaler 200mcg BD"]}),
            # Gopal — Coal worker pneumoconiosis
            HR(worker_id=W["gopal"], record_type="visit", data_json={
                "date":(NOW-timedelta(days=150)).isoformat(),
                "facility":"Korba DH, Chhattisgarh","doctor":"Dr. S. Verma",
                "diagnosis":"Coal Worker Pneumoconiosis + Chronic Bronchitis",
                "vitals":{"bp":"138/90","spo2":89,"fev1":"52%"},
                "prescription":["Prednisolone 5mg OD","Doxycycline 100mg BD"]}),
            # Mohan — Chemical dermatitis
            HR(worker_id=W["mohan"], record_type="visit", data_json={
                "date":(NOW-timedelta(days=40)).isoformat(),
                "facility":"ESI Hospital, Vapi","doctor":"Dr. N. Joshi",
                "diagnosis":"Chemical Contact Dermatitis — bilateral hands and forearms",
                "prescription":["Cetirizine 10mg OD","Clobetasol Cream BD","Barrier Cream"]}),
            # Lakshman — Heat exhaustion
            HR(worker_id=W["lakshman"], record_type="visit", data_json={
                "date":(NOW-timedelta(days=60)).isoformat(),
                "facility":"PHC Haveli, Pune","doctor":"Dr. K. Patil",
                "diagnosis":"Exertional Heat Exhaustion — WBGT exceeded limits",
                "vitals":{"bp":"100/60","temp_c":39.2,"hr":112},
                "treatment":"IV fluids, rest in shade, ORS. Cleared after 4 hours."}),
            # Sunita — Pesticide poisoning
            HR(worker_id=W["sunita"], record_type="visit", data_json={
                "date":(NOW-timedelta(days=35)).isoformat(),
                "facility":"PHC Whitefield, Bengaluru","doctor":"Dr. P. Rajan",
                "diagnosis":"Mild Organophosphate Exposure — cholinesterase reduced",
                "vitals":{"bp":"108/72","hr":88},
                "prescription":["Atropine 0.6mg IM stat","Chlorpheniramine 4mg TID"]}),
            # Raju — Scaffolding fall
            HR(worker_id=W["raju"], record_type="injury", data_json={
                "date":(NOW-timedelta(days=90)).isoformat(),
                "facility":"Apollo Clinic, Bengaluru","type":"Fall from height (2m scaffolding)",
                "description":"L4-L5 disc bulge with radiculopathy",
                "treatment":"Conservative: bed rest, physiotherapy, NSAIDs","days_off":21}),
            # Bharat — Mining noise exposure
            HR(worker_id=W["bharat"], record_type="screening", data_json={
                "date":(NOW-timedelta(days=80)).isoformat(),
                "type":"Audiometry Screening","facility":"ESI Dispensary, Chandrapur",
                "results":{"right_ear":"35dB loss at 4kHz","left_ear":"40dB loss at 4kHz",
                           "classification":"Noise-Induced Hearing Loss — moderate"},
                "recommendation":"Mandatory ear protection, annual audiometry"}),
            # Kamla — COPD
            HR(worker_id=W["kamla"], record_type="lab", data_json={
                "date":(NOW-timedelta(days=25)).isoformat(),
                "facility":"Civil Hospital, Surat",
                "tests":{"spirometry":{"fev1":"62%","fvc":"78%","ratio":"79%"},
                         "chest_xray":"Hyperinflation, flattened diaphragm"},
                "impression":"Moderate COPD — Gold Stage II"}),
            # Savitri — Malnutrition
            HR(worker_id=W["savitri"], record_type="visit", data_json={
                "date":(NOW-timedelta(days=20)).isoformat(),
                "facility":"Urban PHC, Mumbai","doctor":"Dr. A. Desai",
                "diagnosis":"Severe Underweight (BMI 16.8), Vitamin B12 Deficiency",
                "vitals":{"bp":"98/64","hr":84,"weight_kg":38},
                "prescription":["High-calorie supplementary nutrition","Methylcobalamin 1500mcg OD"]}),
            # Geeta — Gastritis
            HR(worker_id=W["geeta"], record_type="visit", data_json={
                "date":(NOW-timedelta(days=50)).isoformat(),
                "facility":"CHC Kalol, Gujarat","doctor":"Dr. H. Shah",
                "diagnosis":"Erosive Gastritis — H. pylori positive",
                "prescription":["Pantoprazole 40mg OD","Amoxicillin 1g BD x 14d","Clarithromycin 500mg BD x 14d"]}),
        ]
        db.add_all(health_records)

        # ================================================================
        #  6. RISK PROFILES (15)
        # ================================================================
        risk_profiles = []
        for key, (occ, tasks, symptoms, years, scores, level) in RISK_DATA.items():
            risk_profiles.append(RiskProfile(
                worker_id=W[key], occupation=occ,
                tasks_json=tasks, symptoms_json=symptoms,
                years_in_job=years, scores_json=scores, risk_level=level,
            ))
        db.add_all(risk_profiles)

        # ================================================================
        #  7. LOCATION LOGS — Migration tracking
        # ================================================================
        location_logs = []
        for key, locs in LOCATIONS.items():
            for i, (state, city, lat, lng) in enumerate(locs):
                location_logs.append(LocationLog(
                    worker_id=W[key], state=state, city=city,
                    latitude=lat, longitude=lng,
                    source="registration" if i == 0 else "gps",
                ))
        db.add_all(location_logs)

        # ================================================================
        #  8. NOTIFICATIONS
        # ================================================================
        notifications = [
            Notification(worker_id=W["ramesh"], channel="sms",
                         message="Ramesh: HbA1c follow-up due 15-Apr. Visit nearest PHC.",
                         status="sent", sent_at=NOW-timedelta(days=2)),
            Notification(worker_id=W["meena"], channel="whatsapp",
                         message="Meena: ANC-3 at 28 weeks. Contact ASHA Anita for transport.",
                         status="queued"),
            Notification(worker_id=W["suresh"], channel="sms",
                         message="Suresh: Safety training 10-Apr at Site #4. Mandatory.",
                         status="sent", sent_at=NOW-timedelta(days=5)),
            Notification(worker_id=W["dinesh"], channel="whatsapp",
                         message="Dinesh: Urgent — spirometry re-test needed. FEV1 declining.",
                         status="sent", sent_at=NOW-timedelta(days=1)),
            Notification(worker_id=W["gopal"], channel="sms",
                         message="Gopal: Annual health screening scheduled at NIOH on 20-Apr.",
                         status="queued"),
            Notification(worker_id=W["parvati"], channel="whatsapp",
                         message="Parvati: Byssinosis follow-up with Dr. Patel on 12-Apr.",
                         status="sent", sent_at=NOW-timedelta(days=3)),
        ]
        db.add_all(notifications)

        await db.commit()
        n_hr = len(health_records)
        n_risk = len(risk_profiles)
        n_loc = len(location_logs)
        n_notif = len(notifications)
        print("✅ Seed data inserted successfully!")
        print(f"   Workers:       {len(WORKERS)} migrant workers across 8 occupations")
        print(f"   Employer:      {employer.name} ({employer.id})")
        print(f"   ASHA Workers:  3")
        print(f"   Doctor:        {doctor.name}")
        print(f"   Health Records:{n_hr}  Risk Profiles:{n_risk}")
        print(f"   Locations:     {n_loc}  Notifications:{n_notif}")


if __name__ == "__main__":
    asyncio.run(seed())

