import { useState } from "react";
import {
  LayoutDashboard,
  Users,
  ClipboardList,
  Calendar,
  FileText,
  Settings,
  Bell,
  AlertTriangle,
  X,
  HeartPulse,
  MapPin,
  Phone,
  Briefcase,
  ShieldCheck,
  Activity,
} from "lucide-react";
import { api } from "../services/api";
import "./AshaDashboard.css";

/* ─── Demo Data ─── */
const WORKERS = [
  {
    id: "SW-100001",
    name: "Ramesh Kumar",
    initials: "RK",
    age: 35,
    phone: "+91-98765-43210",
    occupation: "Stone Cutter",
    state: "Rajasthan",
    status: "healthy",
    lastSeen: "Today, 9:15 AM",
    abha: "91-1234-5678-9012",
    vitals: { bp: "120/80", spo2: "98%", hr: "72 bpm" },
    riskLevel: "Low",
  },
  {
    id: "SW-100002",
    name: "Suresh Patel",
    initials: "SP",
    age: 42,
    phone: "+91-98765-43211",
    occupation: "Construction",
    state: "Bihar",
    status: "at-risk",
    lastSeen: "Yesterday, 4:30 PM",
    abha: "91-2345-6789-0123",
    vitals: { bp: "145/95", spo2: "94%", hr: "88 bpm" },
    riskLevel: "High",
  },
  {
    id: "SW-100003",
    name: "Priya Devi",
    initials: "PD",
    age: 28,
    phone: "+91-98765-43212",
    occupation: "Textile Worker",
    state: "Gujarat",
    status: "healthy",
    lastSeen: "Today, 11:00 AM",
    abha: "91-3456-7890-1234",
    vitals: { bp: "118/76", spo2: "99%", hr: "68 bpm" },
    riskLevel: "Low",
  },
];

const NAV_ITEMS = [
  { label: "Dashboard", icon: LayoutDashboard, active: true },
  { label: "Migrants", icon: Users },
  { label: "Screenings", icon: ClipboardList },
  { label: "Schedule", icon: Calendar },
  { label: "Reports", icon: FileText },
  { label: "Settings", icon: Settings },
];

/* ─── Side Panel ─── */

function WorkerPanel({ worker, onClose }) {
  if (!worker) return null;

  // Derive parameters from backend if available, fallback to mock data
  const backendRec = worker.backend?.worker;
  const backendRisk = worker.backend?.occupational_risk?.[0]?.scores_json;
  
  const displayName = backendRec?.name || worker.name;
  const displayPhone = backendRec?.phone_number || worker.phone;
  const displayState = backendRec?.home_state || worker.state;
  const displayAge = backendRec?.date_of_birth ? (new Date().getFullYear() - new Date(backendRec.date_of_birth).getFullYear()) : worker.age;
  const displayAbha = backendRec?.abha_number || worker.abha;
  
  let riskVal = worker.riskLevel;
  let riskColor = worker.status === "healthy" ? "green" : "orange";
  
  if (backendRisk) {
    const highestRisk = Math.max(...Object.values(backendRisk)) * 100;
    if (highestRisk > 60) {
      riskVal = "High Risk";
      riskColor = "red";
    } else if (highestRisk > 30) {
      riskVal = "Medium Risk";
      riskColor = "orange";
    } else {
      riskVal = "Low Risk";
      riskColor = "green";
    }
  }

  return (
    <>
      <div className="asha-panel-overlay" onClick={onClose} />
      <div className="asha-panel">
        <div className="asha-panel__header">
          <span className="asha-panel__title">Worker Record (Live Sync)</span>
          <button className="asha-panel__close" onClick={onClose}>
            <X size={16} />
          </button>
        </div>

        <div className="asha-panel__body">
          {/* ID Card */}
          <div className="asha-panel__id-card">
            <div className="asha-panel__id-avatar">{worker.initials}</div>
            <div>
              <div className="asha-panel__id-name">{displayName}</div>
              <div className="asha-panel__id-num">SwasthyaID: {worker.id}</div>
              {worker.backend && <span style={{fontSize: '10px', background: '#dcfce7', color: '#166534', padding: '2px 4px', borderRadius: '4px'}}>Backend Synced</span>}
            </div>
          </div>

          {/* Personal Info */}
          <div className="asha-panel__section">
            <div className="asha-panel__section-title">Personal Details</div>
            <div className="asha-panel__fields">
              <div className="asha-panel__field">
                <div className="asha-panel__field-label">Age</div>
                <div className="asha-panel__field-value">{displayAge} yrs</div>
              </div>
              <div className="asha-panel__field">
                <div className="asha-panel__field-label">Phone</div>
                <div className="asha-panel__field-value" style={{ fontSize: "0.78rem" }}>{displayPhone}</div>
              </div>
              <div className="asha-panel__field">
                <div className="asha-panel__field-label">Occupation</div>
                <div className="asha-panel__field-value">{worker.occupation}</div>
              </div>
              <div className="asha-panel__field">
                <div className="asha-panel__field-label">State</div>
                <div className="asha-panel__field-value">{displayState}</div>
              </div>
            </div>
          </div>

          {/* Health Status */}
          <div className="asha-panel__section">
            <div className="asha-panel__section-title">Health Status</div>
            <div className="asha-panel__fields">
              <div className="asha-panel__field">
                <div className="asha-panel__field-label">Status</div>
                <div className="asha-panel__field-value">
                  <span className={`asha-status-dot asha-status-dot--${riskColor}`} />{" "}
                  <span className={`asha-status-label asha-status-label--${riskColor}`}>
                    {riskColor === "green" ? "Healthy" : riskColor === "orange" ? "At Risk" : "Critical"}
                  </span>
                </div>
              </div>
              <div className="asha-panel__field">
                <div className="asha-panel__field-label">KaamSuraksha</div>
                <div className="asha-panel__field-value">{riskVal}</div>
              </div>
              <div className="asha-panel__field" style={{ gridColumn: "1 / -1" }}>
                <div className="asha-panel__field-label">ABHA Number</div>
                <div className="asha-panel__field-value" style={{ fontFamily: "monospace" }}>{displayAbha}</div>
              </div>
            </div>
          </div>

          {/* Vitals */}
          <div className="asha-panel__section">
            <div className="asha-panel__section-title">Latest Vitals</div>
            <div className="asha-panel__vitals">
              <div className="asha-panel__vital">
                <div className="asha-panel__vital-val">{worker.vitals.bp}</div>
                <div className="asha-panel__vital-label">Blood Pressure</div>
              </div>
              <div className="asha-panel__vital">
                <div className="asha-panel__vital-val">{worker.vitals.spo2}</div>
                <div className="asha-panel__vital-label">SpO₂</div>
              </div>
              <div className="asha-panel__vital">
                <div className="asha-panel__vital-val">{worker.vitals.hr}</div>
                <div className="asha-panel__vital-label">Heart Rate</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

/* ─── Main Component ─── */

export default function AshaDashboard() {
  const [selectedWorker, setSelectedWorker] = useState(null);

  const handleWorkerSelect = async (worker) => {
    // Show loading state or immediately fetch
    try {
      const record = await api.getWorkerRecord(worker.id);
      setSelectedWorker({ ...worker, backend: record });
    } catch (err) {
      console.warn("Could not fetch real record, falling back to mock UI");
      setSelectedWorker(worker);
    }
  };

  return (
    <div className="asha-layout">
      {/* ── Sidebar ── */}
      <aside className="asha-sidebar">
        <div className="asha-sidebar__brand">
          <div className="asha-sidebar__brand-icon">
            <HeartPulse size={18} />
          </div>
          SwasthyaSetu
        </div>

        <ul className="asha-sidebar__nav">
          {NAV_ITEMS.map((item) => (
            <li
              key={item.label}
              className={`asha-sidebar__item ${item.active ? "asha-sidebar__item--active" : ""}`}
            >
              <item.icon size={18} />
              {item.label}
            </li>
          ))}
        </ul>

        <div className="asha-sidebar__footer">
          <div className="asha-sidebar__avatar">AS</div>
          <div>
            <div className="asha-sidebar__user-name">Anita Sharma</div>
            <div className="asha-sidebar__user-role">ASHA Worker</div>
          </div>
        </div>
      </aside>

      {/* ── Main ── */}
      <div className="asha-main">
        {/* Top Nav */}
        <header className="asha-topnav">
          <h1 className="asha-topnav__title">
            ASHA Dashboard
            <span className="asha-topnav__badge">
              <ShieldCheck size={12} /> Verified
            </span>
          </h1>
          <div className="asha-topnav__actions">
            <button className="asha-topnav__bell">
              <Bell size={18} />
              <span className="asha-topnav__bell-dot" />
            </button>
          </div>
        </header>

        {/* Content */}
        <div className="asha-content">
          {/* Stats Row */}
          <div className="asha-stats">
            <div className="asha-stat-card">
              <div className="asha-stat-card__header">
                <span className="asha-stat-card__title">Village Overview</span>
                <div className="asha-stat-card__icon-wrap asha-stat-card__icon-wrap--green">
                  <MapPin size={18} />
                </div>
              </div>
              <div className="asha-stat-card__metrics">
                <div>
                  <div className="asha-metric__value asha-metric__value--blue">150</div>
                  <div className="asha-metric__label">Total Registered</div>
                </div>
                <div>
                  <div className="asha-metric__value asha-metric__value--orange">45</div>
                  <div className="asha-metric__label">Migrated Workers</div>
                </div>
              </div>
            </div>

            <div className="asha-stat-card">
              <div className="asha-stat-card__header">
                <span className="asha-stat-card__title">Screenings</span>
                <div className="asha-stat-card__icon-wrap asha-stat-card__icon-wrap--blue">
                  <Activity size={18} />
                </div>
              </div>
              <div className="asha-stat-card__metrics">
                <div>
                  <div className="asha-metric__value asha-metric__value--blue">12</div>
                  <div className="asha-metric__label">Completed Today</div>
                </div>
                <div>
                  <div className="asha-metric__value asha-metric__value--orange">8</div>
                  <div className="asha-metric__label">Pending</div>
                </div>
              </div>
            </div>

            <div className="asha-stat-card">
              <div className="asha-stat-card__header">
                <span className="asha-stat-card__title">Quick Actions</span>
                <div className="asha-stat-card__icon-wrap asha-stat-card__icon-wrap--orange">
                  <Briefcase size={18} />
                </div>
              </div>
              <div className="asha-stat-card__metrics">
                <div>
                  <div className="asha-metric__value asha-metric__value--blue">3</div>
                  <div className="asha-metric__label">Follow-ups Due</div>
                </div>
                <div>
                  <div className="asha-metric__value asha-metric__value--orange">2</div>
                  <div className="asha-metric__label">Referrals</div>
                </div>
              </div>
            </div>
          </div>

          {/* Migrant List */}
          <div className="asha-table-card">
            <div className="asha-table-card__header">
              <span className="asha-table-card__title">Migrant Workers (Auto-Synced with backend)</span>
              <span className="asha-table-card__count">{WORKERS.length} workers</span>
            </div>
            <table className="asha-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Status</th>
                  <th>Occupation</th>
                  <th>Last Seen</th>
                  <th>SwasthyaID</th>
                </tr>
              </thead>
              <tbody>
                {WORKERS.map((w) => {
                  const color = w.status === "healthy" ? "green" : "orange";
                  return (
                    <tr key={w.id} onClick={() => handleWorkerSelect(w)}>
                      <td>
                        <div className="asha-table__name-cell">
                          <div className={`asha-table__avatar asha-table__avatar--${color}`}>
                            {w.initials}
                          </div>
                          {w.name}
                        </div>
                      </td>
                      <td>
                        <span className={`asha-status-dot asha-status-dot--${color}`} />
                        <span className={`asha-status-label asha-status-label--${color}`}>
                          {w.status === "healthy" ? "Healthy" : "At Risk"}
                        </span>
                      </td>
                      <td>{w.occupation}</td>
                      <td>{w.lastSeen}</td>
                      <td style={{ fontFamily: "monospace", fontSize: "0.8rem" }}>{w.id}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {/* Alert */}
          <div className="asha-alert">
            <div className="asha-alert__icon">
              <AlertTriangle size={20} />
            </div>
            <div className="asha-alert__text">
              <div className="asha-alert__title">3 workers returning — schedule follow-up</div>
              <div className="asha-alert__desc">Ramesh K., Suresh P., and 1 other need re-screening upon return</div>
            </div>
            <button className="asha-alert__btn">Schedule</button>
          </div>
        </div>
      </div>

      {/* Worker Panel */}
      <WorkerPanel worker={selectedWorker} onClose={() => setSelectedWorker(null)} />
    </div>
  );
}
