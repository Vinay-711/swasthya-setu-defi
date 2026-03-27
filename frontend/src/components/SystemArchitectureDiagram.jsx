import {
  Smartphone,
  Monitor,
  Phone,
  MessageSquare,
  Shield,
  Gauge,
  GitBranch,
  Scale,
  Fingerprint,
  HeartPulse,
  Brain,
  Languages,
  FileText,
  Bell,
  Database,
  HardDrive,
  Layers,
  Archive,
  Cpu,
  Globe,
  Server,
  Lock,
  ArrowDown,
  CheckCircle2,
} from "lucide-react";
import "./SystemArchitectureDiagram.css";

/* ─── Data ─── */

const CLIENT_ITEMS = [
  { name: "Flutter Mobile App", desc: "Android / iOS", Icon: Smartphone },
  { name: "React Web Dashboard", desc: "ASHA / Doctor / Admin", Icon: Monitor },
  { name: "IVR System", desc: "Voice Calls", Icon: Phone },
  { name: "WhatsApp Bot", desc: "Chat Interface", Icon: MessageSquare },
];

const GATEWAY_FEATURES = [
  { label: "Authentication", Icon: Shield },
  { label: "Rate Limiting", Icon: Gauge },
  { label: "Routing", Icon: GitBranch },
  { label: "Load Balancing", Icon: Scale },
];

const MICROSERVICES = [
  { name: "Identity", tech: "Node.js", Icon: Fingerprint },
  { name: "Health", tech: "Node.js", Icon: HeartPulse },
  { name: "AI / ML", tech: "Python", Icon: Brain },
  { name: "Translation", tech: "Python", Icon: Languages },
  { name: "Document", tech: "Python", Icon: FileText },
  { name: "Notification", tech: "Node.js", Icon: Bell },
];

const DATA_ITEMS = [
  { name: "PostgreSQL", tech: "Primary DB", Icon: Database },
  { name: "MongoDB", tech: "Documents", Icon: HardDrive },
  { name: "Redis", tech: "Cache", Icon: Layers },
  { name: "S3 / MinIO", tech: "File Storage", Icon: Archive },
];

const BOTTOM_CARDS = [
  {
    title: "AI / ML Models",
    color: "amber",
    Icon: Cpu,
    body: "Whisper, LayoutLMv3, XGBoost",
  },
  {
    title: "External APIs",
    color: "teal",
    Icon: Globe,
    body: "ABDM, e-Sanjeevani, PMJAY",
  },
  {
    title: "Infrastructure",
    color: "pink",
    Icon: Server,
    body: "AWS EKS, Kubernetes",
  },
  {
    title: "Security",
    color: "sky",
    Icon: Lock,
    body: "AES-256, DPDP Compliant",
  },
];

/* ─── Sub-components ─── */

function CellCard({ Icon, name, desc, colorClass }) {
  return (
    <div className="arch-cell">
      <div className={`arch-cell__icon arch-cell__icon--${colorClass}`}>
        <Icon size={18} />
      </div>
      <div className="arch-cell__text">
        <span className="arch-cell__name">{name}</span>
        {desc && <span className="arch-cell__desc">{desc}</span>}
      </div>
    </div>
  );
}

function MiniCard({ Icon, name, tech, colorClass }) {
  return (
    <div className="arch-mini-card">
      <div className={`arch-mini-card__icon arch-mini-card__icon--${colorClass}`}>
        <Icon size={16} />
      </div>
      <span className="arch-mini-card__name">{name}</span>
      <span className="arch-mini-card__tech">{tech}</span>
    </div>
  );
}

/* ─── Main Component ─── */

export default function SystemArchitectureDiagram() {
  return (
    <section className="arch-diagram">
      <h2 className="arch-diagram__title">System Architecture</h2>
      <p className="arch-diagram__subtitle">
        Microservices-based architecture powering SwasthyaSetu
      </p>

      {/* ── 4 Columns ── */}
      <div className="arch-columns">
        {/* Client Layer */}
        <div className="arch-col">
          <div className="arch-col__header arch-col__header--blue">
            <span className="arch-col__header-icon">
              <Smartphone size={18} />
            </span>
            Client Layer
          </div>
          <div className="arch-col__body">
            {CLIENT_ITEMS.map((c) => (
              <CellCard key={c.name} Icon={c.Icon} name={c.name} desc={c.desc} colorClass="blue" />
            ))}
          </div>
        </div>

        {/* API Gateway */}
        <div className="arch-col">
          <div className="arch-col__header arch-col__header--purple">
            <span className="arch-col__header-icon">
              <Shield size={18} />
            </span>
            API Gateway
          </div>
          <div className="arch-col__body">
            <CellCard
              Icon={GitBranch}
              name="Kong / AWS API Gateway"
              desc="Unified entry point"
              colorClass="purple"
            />
            <ul className="arch-features">
              {GATEWAY_FEATURES.map((f) => (
                <li key={f.label}>
                  <CheckCircle2 size={14} />
                  {f.label}
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Microservices */}
        <div className="arch-col">
          <div className="arch-col__header arch-col__header--purple">
            <span className="arch-col__header-icon">
              <Layers size={18} />
            </span>
            Microservices
          </div>
          <div className="arch-col__body">
            <div className="arch-mini-grid arch-mini-grid--2x3">
              {MICROSERVICES.map((s) => (
                <MiniCard
                  key={s.name}
                  Icon={s.Icon}
                  name={s.name}
                  tech={s.tech}
                  colorClass="purple"
                />
              ))}
            </div>
          </div>
        </div>

        {/* Data Layer */}
        <div className="arch-col">
          <div className="arch-col__header arch-col__header--green">
            <span className="arch-col__header-icon">
              <Database size={18} />
            </span>
            Data Layer
          </div>
          <div className="arch-col__body">
            <div className="arch-mini-grid arch-mini-grid--2x2">
              {DATA_ITEMS.map((d) => (
                <MiniCard
                  key={d.name}
                  Icon={d.Icon}
                  name={d.name}
                  tech={d.tech}
                  colorClass="green"
                />
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* ── Connector Arrows ── */}
      <div className="arch-connectors">
        <ArrowDown size={22} />
        <ArrowDown size={22} />
        <ArrowDown size={22} />
        <ArrowDown size={22} />
      </div>

      {/* ── Bottom Layer ── */}
      <div className="arch-bottom">
        {BOTTOM_CARDS.map((card) => (
          <div key={card.title} className="arch-bottom-card">
            <div className={`arch-bottom-card__header arch-bottom-card__header--${card.color}`}>
              <span className="arch-bottom-card__header-icon">
                <card.Icon size={16} />
              </span>
              {card.title}
            </div>
            <div className="arch-bottom-card__body">{card.body}</div>
          </div>
        ))}
      </div>
    </section>
  );
}
