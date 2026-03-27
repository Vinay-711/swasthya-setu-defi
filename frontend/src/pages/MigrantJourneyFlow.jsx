import React, { useEffect, useState } from 'react';
import {
  MapPin, ArrowRight, Users, Stethoscope, Building2, HeartPulse,
  ClipboardCheck, Mic, Navigation, Bell, QrCode, FileText, Languages,
  RefreshCw, CalendarCheck, Link2
} from 'lucide-react';

const stages = [
  {
    label: 'SOURCE',
    location: 'Odisha Village',
    bg: '#2D8C4E',
    border: '#1A6B38',
    items: [
      { icon: ClipboardCheck, text: 'Registration' },
      { icon: Link2, text: 'ABHA Link' },
      { icon: Mic, text: 'Voice Record' },
    ],
  },
  {
    label: 'MIGRATION',
    location: 'To Bengaluru',
    bg: '#E5681A',
    border: '#C4520E',
    items: [
      { icon: Navigation, text: 'Location Update' },
      { icon: Bell, text: 'ASHA Alert' },
    ],
  },
  {
    label: 'DESTINATION',
    location: 'Karnataka PHC',
    bg: '#2563EB',
    border: '#1D4ED8',
    items: [
      { icon: QrCode, text: 'QR Scan' },
      { icon: FileText, text: 'History Access' },
      { icon: Languages, text: 'Translation' },
    ],
  },
  {
    label: 'RETURN',
    location: 'Back to Odisha',
    bg: '#7C3AED',
    border: '#6D28D9',
    items: [
      { icon: RefreshCw, text: 'Data Sync' },
      { icon: CalendarCheck, text: 'Follow-up' },
      { icon: Link2, text: 'Continuity' },
    ],
  },
];

const actors = [
  {
    icon: Users,
    name: 'Migrant Worker',
    desc: 'Primary user who carries health data across state borders via QR code and voice interface.',
    color: '#E5681A',
  },
  {
    icon: HeartPulse,
    name: 'ASHA Worker',
    desc: 'Community health worker who registers workers at source and monitors migration alerts.',
    color: '#2D8C4E',
  },
  {
    icon: Stethoscope,
    name: 'Doctor',
    desc: 'PHC physician at destination who scans QR, views history, and uses real-time translation.',
    color: '#2563EB',
  },
  {
    icon: Building2,
    name: 'Employer',
    desc: 'Construction site employer tracking worker wellness and occupational risk compliance.',
    color: '#7C3AED',
  },
];

function StageCard({ stage, index, visible }) {
  const Icon = MapPin;
  return (
    <div
      className={`
        flex flex-col rounded-xl overflow-hidden shadow-lg border-2
        transition-all duration-500 ease-out min-w-[200px] flex-1
        ${visible ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-8'}
      `}
      style={{ borderColor: stage.border }}
    >
      {/* Colored header */}
      <div
        className="px-4 py-3 flex items-center gap-2"
        style={{ backgroundColor: stage.bg }}
      >
        <Icon size={18} className="text-white" />
        <div>
          <div className="text-white font-bold text-sm tracking-wide">{stage.label}</div>
          <div className="text-white/80 text-xs">{stage.location}</div>
        </div>
      </div>

      {/* Sub-items */}
      <div className="bg-white px-4 py-3 flex flex-col gap-2 flex-1">
        {stage.items.map((item, i) => {
          const ItemIcon = item.icon;
          return (
            <div key={i} className="flex items-center gap-2 text-gray-700 text-sm">
              <ItemIcon size={16} style={{ color: stage.bg }} />
              <span className="font-medium">{item.text}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function ActorCard({ actor }) {
  const Icon = actor.icon;
  return (
    <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 flex items-start gap-3">
      <div
        className="w-10 h-10 rounded-full flex items-center justify-center shrink-0"
        style={{ backgroundColor: actor.color + '18' }}
      >
        <Icon size={20} style={{ color: actor.color }} />
      </div>
      <div>
        <div className="font-semibold text-gray-800 text-sm">{actor.name}</div>
        <div className="text-gray-500 text-xs leading-relaxed mt-0.5">{actor.desc}</div>
      </div>
    </div>
  );
}

export default function MigrantJourneyFlow() {
  const [visibleStages, setVisibleStages] = useState([]);

  useEffect(() => {
    stages.forEach((_, i) => {
      setTimeout(() => {
        setVisibleStages(prev => [...prev, i]);
      }, 200 * (i + 1));
    });
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 p-6 font-[Inter,sans-serif]">
      {/* Page Title */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Migrant Health Journey</h1>
        <p className="text-gray-500 mt-1 text-sm">End-to-end health data continuity across state borders</p>
      </div>

      <div className="flex flex-col xl:flex-row gap-8">
        {/* Main flow area */}
        <div className="flex-1">
          {/* Horizontal stage flow — stacks vertically on mobile */}
          <div className="flex flex-col md:flex-row items-stretch gap-0">
            {stages.map((stage, i) => (
              <div key={i} className="flex flex-col md:flex-row items-center">
                <StageCard
                  stage={stage}
                  index={i}
                  visible={visibleStages.includes(i)}
                />
                {/* Arrow between stages */}
                {i < stages.length - 1 && (
                  <>
                    {/* Desktop arrow (horizontal) */}
                    <div className="hidden md:flex items-center px-2 text-gray-400">
                      <ArrowRight size={24} />
                    </div>
                    {/* Mobile arrow (vertical) */}
                    <div className="flex md:hidden items-center justify-center py-2 text-gray-400 rotate-90">
                      <ArrowRight size={24} />
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>

          {/* Timeline badge */}
          <div className="mt-6 flex justify-end">
            <div className="bg-gray-800 text-white text-xs font-semibold px-4 py-2 rounded-full shadow-md">
              ⏱ Complete cycle: 6–12 months
            </div>
          </div>
        </div>

        {/* Key Actors Sidebar */}
        <div className="w-full xl:w-72 shrink-0">
          <h2 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4">Key Actors</h2>
          <div className="flex flex-col gap-3">
            {actors.map((actor, i) => (
              <ActorCard key={i} actor={actor} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
