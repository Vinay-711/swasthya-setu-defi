import { useEffect, useRef, useState } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
} from "recharts";
import {
  Factory,
  Users,
  Download,
  ShieldCheck,
  AlertTriangle,
  HardHat,
  Pickaxe,
  Paintbrush,
  RefreshCw,
} from "lucide-react";
import "./EmployerPortal.css";

/* ── Register Chart.js components ── */
ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

/* ── Fallback demo data ── */
const DEMO_DATA = {
  employerName: "Sunrise Construction Pvt Ltd",
  totalWorkers: 250,
  healthStatus: {
    healthy: 180,
    atRisk: 50,
    critical: 20,
  },
  compliance: {
    percentage: 95,
    ppe: 98,
    screenings: 92,
    training: 95,
  },
  topRiskOccupations: [
    { rank: 1, name: "Stone Cutting", workers: 45, riskScore: 8.7, detail: "Silicosis, respiratory exposure" },
    { rank: 2, name: "Welding & Metal Work", workers: 32, riskScore: 7.2, detail: "Fume inhalation, burn risk" },
    { rank: 3, name: "Scaffolding & Heights", workers: 28, riskScore: 6.5, detail: "Fall hazard, heat exhaustion" },
  ],
};

/* ── Compliance Gauge ── */
function ComplianceGauge({ percentage }) {
  const gaugeData = [
    { name: "Compliant", value: percentage },
    { name: "Gap", value: 100 - percentage },
  ];
  const COLORS = ["#059669", "#e2e8f0"];

  return (
    <ResponsiveContainer width="100%" height="100%">
      <PieChart>
        <Pie
          data={gaugeData}
          cx="50%"
          cy="50%"
          startAngle={90}
          endAngle={-270}
          innerRadius="70%"
          outerRadius="90%"
          dataKey="value"
          stroke="none"
        >
          {gaugeData.map((_, i) => (
            <Cell key={i} fill={COLORS[i]} />
          ))}
        </Pie>
      </PieChart>
    </ResponsiveContainer>
  );
}

/* ── Main Component ── */
export default function EmployerPortal() {
  const [data, setData] = useState(DEMO_DATA);
  const [loading, setLoading] = useState(false);
  const printRef = useRef(null);

  /* Wire to backend API */
  useEffect(() => {
    const employerId = "employer-001";
    setLoading(true);
    fetch(`/api/v1/employer/dashboard/${employerId}`)
      .then((r) => {
        if (!r.ok) throw new Error("API not available");
        return r.json();
      })
      .then((json) => setData(json))
      .catch(() => {
        /* Fallback to demo data */
        setData(DEMO_DATA);
      })
      .finally(() => setLoading(false));
  }, []);

  /* Chart.js horizontal bar data */
  const barData = {
    labels: ["Healthy", "At Risk", "Critical"],
    datasets: [
      {
        label: "Workers",
        data: [
          data.healthStatus.healthy,
          data.healthStatus.atRisk,
          data.healthStatus.critical,
        ],
        backgroundColor: ["#059669", "#F59E0B", "#DC2626"],
        borderRadius: 6,
        barThickness: 32,
      },
    ],
  };

  const barOptions = {
    indexAxis: "y",
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: "#0f172a",
        titleFont: { family: "Inter", weight: "600" },
        bodyFont: { family: "Inter" },
        padding: 10,
        cornerRadius: 8,
      },
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: {
          font: { family: "Inter", size: 12 },
          color: "#94a3b8",
        },
      },
      y: {
        grid: { display: false },
        ticks: {
          font: { family: "Inter", size: 13, weight: "600" },
          color: "#334155",
        },
      },
    },
  };

  const handleExport = () => {
    window.print();
  };

  return (
    <div className="emp-shell" ref={printRef}>
      {/* ── Top Bar ── */}
      <header className="emp-topbar">
        <div className="emp-topbar__left">
          <div className="emp-topbar__logo">
            <Factory size={20} />
          </div>
          <div>
            <div className="emp-topbar__title">Employer Portal</div>
            <div className="emp-topbar__subtitle">{data.employerName}</div>
          </div>
        </div>
        <div className="emp-topbar__actions">
          <button className="emp-btn emp-btn--outline" onClick={() => window.location.reload()}>
            <RefreshCw size={14} /> Refresh
          </button>
          <button className="emp-btn emp-btn--primary" onClick={handleExport}>
            <Download size={14} /> Download Compliance Report (PDF)
          </button>
        </div>
      </header>

      {/* ── Main Content ── */}
      <div className="emp-content">
        {/* Hero Metric */}
        <div className="emp-hero">
          <div>
            <div className="emp-hero__value">{data.totalWorkers}</div>
            <div className="emp-hero__label">Registered Workers</div>
          </div>
          <div className="emp-hero__icon">
            <Users size={32} />
          </div>
        </div>

        {/* Two-Column Grid */}
        <div className="emp-grid">
          {/* Health Status Chart */}
          <div className="emp-card">
            <div className="emp-card__header">
              <span className="emp-card__title">Health Status Overview</span>
              <span className="emp-card__badge emp-card__badge--green">
                {data.healthStatus.healthy} healthy
              </span>
            </div>
            <div className="emp-card__body">
              <div className="emp-chart-wrap">
                <Bar data={barData} options={barOptions} />
              </div>
            </div>
          </div>

          {/* Compliance Gauge */}
          <div className="emp-card">
            <div className="emp-card__header">
              <span className="emp-card__title">Compliance Score</span>
              <span className="emp-card__badge emp-card__badge--green">
                <ShieldCheck size={12} style={{ marginRight: 4 }} />
                {data.compliance.percentage}% Compliant
              </span>
            </div>
            <div className="emp-card__body">
              <div className="emp-gauge-section">
                <div className="emp-gauge-wrap">
                  <ComplianceGauge percentage={data.compliance.percentage} />
                </div>
                <div className="emp-gauge-info">
                  <div className="emp-gauge-info__value">{data.compliance.percentage}%</div>
                  <div className="emp-gauge-info__label">Overall Compliance</div>
                  <div className="emp-gauge-info__items">
                    <div className="emp-gauge-info__item">
                      <span className="emp-gauge-info__dot" style={{ background: "#059669" }} />
                      PPE Compliance — {data.compliance.ppe}%
                    </div>
                    <div className="emp-gauge-info__item">
                      <span className="emp-gauge-info__dot" style={{ background: "#2563eb" }} />
                      Health Screenings — {data.compliance.screenings}%
                    </div>
                    <div className="emp-gauge-info__item">
                      <span className="emp-gauge-info__dot" style={{ background: "#7c3aed" }} />
                      Safety Training — {data.compliance.training}%
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* KaamSuraksha — Top Risk Occupations */}
        <div className="emp-card" style={{ marginBottom: 24 }}>
          <div className="emp-card__header">
            <span className="emp-card__title">KaamSuraksha — Top Risk Occupations</span>
            <span className="emp-card__badge" style={{ background: "#fef2f2", color: "#dc2626" }}>
              <AlertTriangle size={12} style={{ marginRight: 4 }} /> Risk Monitor
            </span>
          </div>
          <div className="emp-card__body">
            <div className="emp-risk-list">
              {data.topRiskOccupations.map((occ) => {
                const icons = [Pickaxe, HardHat, Paintbrush];
                const Icon = icons[occ.rank - 1] || HardHat;
                const scoreClass =
                  occ.riskScore >= 8 ? "high" : occ.riskScore >= 7 ? "medium" : "low";
                return (
                  <div className="emp-risk-item" key={occ.rank}>
                    <div className={`emp-risk-rank emp-risk-rank--${occ.rank}`}>
                      #{occ.rank}
                    </div>
                    <Icon size={20} style={{ color: "#64748b" }} />
                    <div className="emp-risk-info">
                      <div className="emp-risk-name">{occ.name}</div>
                      <div className="emp-risk-detail">
                        {occ.workers} workers • {occ.detail}
                      </div>
                    </div>
                    <div className={`emp-risk-score emp-risk-score--${scoreClass}`}>
                      {occ.riskScore}/10
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
