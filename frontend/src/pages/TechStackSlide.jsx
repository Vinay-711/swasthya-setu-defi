import React from 'react';
import {
  Monitor, Server, Brain, Database, Cloud, Plug,
  Smartphone, Layout, Layers, Code2, Cpu, FileSearch,
  BarChart3, HardDrive, FileText, Search,
  Container, GitBranch, Workflow,
  Landmark, Languages, MessageSquare
} from 'lucide-react';

const cards = [
  {
    title: 'Frontend',
    bg: '#2563EB',
    border: '#1D4ED8',
    icon: Monitor,
    items: [
      { icon: Smartphone, label: 'Mobile App', value: 'Flutter/Dart — cross-platform iOS/Android' },
      { icon: Layout, label: 'Web Dashboard', value: 'React + TypeScript + Tailwind CSS' },
      { icon: Layers, label: 'State Management', value: 'Redux Toolkit, Riverpod' },
    ],
  },
  {
    title: 'Backend',
    bg: '#2D8C4E',
    border: '#1A6B38',
    icon: Server,
    items: [
      { icon: Code2, label: 'API Services', value: 'Node.js + Express — Identity, Health, Notify' },
      { icon: Cpu, label: 'AI/ML Services', value: 'Python + FastAPI — OCR, Translation, Prediction' },
      { icon: Workflow, label: 'API Gateway', value: 'Kong / AWS API Gateway' },
    ],
  },
  {
    title: 'AI/ML',
    bg: '#7C3AED',
    border: '#6D28D9',
    icon: Brain,
    items: [
      { icon: MessageSquare, label: 'Speech-to-Text', value: 'Whisper + IndicWav2Vec — 12 languages' },
      { icon: FileSearch, label: 'Document OCR', value: 'LayoutLMv3 + Tesseract' },
      { icon: BarChart3, label: 'Risk Prediction', value: 'XGBoost + TensorFlow' },
    ],
  },
  {
    title: 'Database',
    bg: '#E5681A',
    border: '#C4520E',
    icon: Database,
    items: [
      { icon: HardDrive, label: 'Primary DB', value: 'PostgreSQL — Structured data' },
      { icon: FileText, label: 'Document Store', value: 'MongoDB — Medical records' },
      { icon: Search, label: 'Cache & Search', value: 'Redis, Elasticsearch' },
    ],
  },
  {
    title: 'Cloud & DevOps',
    bg: '#0D9488',
    border: '#0F766E',
    icon: Cloud,
    items: [
      { icon: Cloud, label: 'Cloud Provider', value: 'AWS — EKS, RDS, S3, Lambda' },
      { icon: Container, label: 'Orchestration', value: 'Kubernetes EKS + Docker' },
      { icon: GitBranch, label: 'CI/CD', value: 'GitHub Actions, ArgoCD' },
    ],
  },
  {
    title: 'Integrations',
    bg: '#D97706',
    border: '#B45309',
    icon: Plug,
    items: [
      { icon: Landmark, label: 'Government', value: 'ABDM/ABHA, e-Sanjeevani, PMJAY' },
      { icon: Languages, label: 'Translation', value: 'Bhashini API — 22 languages' },
      { icon: MessageSquare, label: 'Communication', value: 'Twilio, WhatsApp Business API' },
    ],
  },
];

function TechCard({ card }) {
  const HeaderIcon = card.icon;

  return (
    <div
      className="group bg-white rounded-2xl overflow-hidden shadow-sm border border-gray-100
                 transition-all duration-300 ease-out
                 hover:shadow-xl hover:-translate-y-1"
      style={{ '--card-color': card.bg, '--card-border': card.border }}
      onMouseEnter={(e) => (e.currentTarget.style.borderColor = card.border)}
      onMouseLeave={(e) => (e.currentTarget.style.borderColor = '#f3f4f6')}
    >
      {/* Colored header badge */}
      <div
        className="px-5 py-3 flex items-center gap-3"
        style={{ backgroundColor: card.bg }}
      >
        <HeaderIcon size={20} className="text-white" />
        <span className="text-white font-bold text-base tracking-wide">{card.title}</span>
      </div>

      {/* Items */}
      <div className="px-5 py-4 flex flex-col divide-y divide-gray-100">
        {card.items.map((item, i) => {
          const ItemIcon = item.icon;
          return (
            <div key={i} className="flex items-start gap-3 py-3 first:pt-0 last:pb-0">
              <div
                className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 mt-0.5"
                style={{ backgroundColor: card.bg + '14' }}
              >
                <ItemIcon size={16} style={{ color: card.bg }} />
              </div>
              <div className="min-w-0">
                <div className="text-sm font-semibold text-gray-800">{item.label}</div>
                <div className="text-xs text-gray-500 leading-relaxed mt-0.5">{item.value}</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default function TechStackSlide() {
  return (
    <div className="min-h-screen bg-gray-50 p-6 md:p-10 font-[Inter,sans-serif]">
      {/* Title */}
      <div className="text-center mb-10">
        <h1 className="text-3xl font-extrabold text-gray-900">Technology Stack</h1>
        <p className="text-gray-500 mt-2 text-sm max-w-xl mx-auto">
          Full-stack architecture powering SwasthyaSetu's migrant health platform
        </p>
      </div>

      {/* 2x3 Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 max-w-6xl mx-auto">
        {cards.map((card, i) => (
          <TechCard key={i} card={card} />
        ))}
      </div>
    </div>
  );
}
