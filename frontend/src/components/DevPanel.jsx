import React, { useState } from 'react';
import { Settings, X, RotateCcw, User, ToggleLeft, ToggleRight } from 'lucide-react';

const DEMO_WORKERS = [
  { id: 'ramesh', name: 'Ramesh K.', swasthyaId: 'SW-100001', role: 'Mason — Diabetes + Hypertension' },
  { id: 'suresh', name: 'Suresh P.', swasthyaId: 'SW-100002', role: 'Rebar Worker — Asthma + Back Pain' },
  { id: 'meena',  name: 'Meena D.', swasthyaId: 'SW-100003', role: 'Domestic — Anemia + ANC' },
];

export default function DevPanel({ mockMode, onToggleMockMode, activeWorker, onSelectWorker, onResetData }) {
  const [open, setOpen] = useState(false);

  // Only show in development
  if (import.meta.env.PROD) return null;

  return (
    <>
      {/* Floating toggle button */}
      <button
        onClick={() => setOpen(!open)}
        style={{
          position: 'fixed', bottom: 20, right: 20, zIndex: 9999,
          width: 48, height: 48, borderRadius: '50%',
          background: '#111827', color: '#fbbf24', border: 'none',
          boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
          cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center',
        }}
        title="Dev Panel"
      >
        {open ? <X size={20} /> : <Settings size={20} />}
      </button>

      {/* Panel */}
      {open && (
        <div style={{
          position: 'fixed', bottom: 80, right: 20, zIndex: 9998,
          width: 300, background: '#1f2937', color: '#f9fafb',
          borderRadius: 16, boxShadow: '0 8px 30px rgba(0,0,0,0.4)',
          fontFamily: 'Inter, sans-serif', overflow: 'hidden',
        }}>
          {/* Header */}
          <div style={{
            padding: '12px 16px', borderBottom: '1px solid #374151',
            display: 'flex', alignItems: 'center', gap: 8,
          }}>
            <Settings size={16} color="#fbbf24" />
            <span style={{ fontWeight: 700, fontSize: 14 }}>Dev Panel</span>
            <span style={{
              marginLeft: 'auto', fontSize: 10, background: '#fbbf24', color: '#111827',
              padding: '2px 8px', borderRadius: 999, fontWeight: 600,
            }}>DEV</span>
          </div>

          {/* Mock API Toggle */}
          <div style={{
            padding: '12px 16px', borderBottom: '1px solid #374151',
            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          }}>
            <span style={{ fontSize: 13, fontWeight: 500 }}>Mock APIs</span>
            <button
              onClick={onToggleMockMode}
              style={{
                background: 'none', border: 'none', cursor: 'pointer',
                color: mockMode ? '#34d399' : '#6b7280', display: 'flex', alignItems: 'center', gap: 6,
              }}
            >
              {mockMode ? <ToggleRight size={24} /> : <ToggleLeft size={24} />}
              <span style={{ fontSize: 12, fontWeight: 600 }}>{mockMode ? 'ON' : 'OFF'}</span>
            </button>
          </div>

          {/* Worker Selector */}
          <div style={{ padding: '12px 16px', borderBottom: '1px solid #374151' }}>
            <div style={{ fontSize: 13, fontWeight: 500, marginBottom: 8 }}>Demo Worker</div>
            {DEMO_WORKERS.map((w) => (
              <button
                key={w.id}
                onClick={() => onSelectWorker?.(w)}
                style={{
                  width: '100%', textAlign: 'left',
                  background: activeWorker?.id === w.id ? '#374151' : 'transparent',
                  border: activeWorker?.id === w.id ? '1px solid #6366f1' : '1px solid transparent',
                  borderRadius: 8, padding: '8px 10px', marginBottom: 4,
                  cursor: 'pointer', color: '#f9fafb', display: 'flex', alignItems: 'center', gap: 8,
                }}
              >
                <User size={14} color={activeWorker?.id === w.id ? '#a5b4fc' : '#6b7280'} />
                <div>
                  <div style={{ fontSize: 13, fontWeight: 600 }}>{w.name}</div>
                  <div style={{ fontSize: 10, color: '#9ca3af' }}>{w.role}</div>
                </div>
              </button>
            ))}
          </div>

          {/* Reset */}
          <div style={{ padding: '12px 16px' }}>
            <button
              onClick={() => {
                if (confirm('Reset all local data? This clears localStorage and reloads.')) {
                  onResetData?.();
                  localStorage.clear();
                  window.location.reload();
                }
              }}
              style={{
                width: '100%', padding: '8px 12px', borderRadius: 8,
                background: '#dc2626', color: 'white', border: 'none',
                cursor: 'pointer', fontWeight: 600, fontSize: 13,
                display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6,
              }}
            >
              <RotateCcw size={14} />
              Reset All Data
            </button>
          </div>
        </div>
      )}
    </>
  );
}
