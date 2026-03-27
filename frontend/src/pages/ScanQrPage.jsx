import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { tr } from "../services/i18n";

// Ensure we fetch from our environment API Base
const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

export default function ScanQrPage({ t }) {
  const [input, setInput] = useState("");
  const [qrUrl, setQrUrl] = useState("");
  const navigate = useNavigate();

  const handleGenerate = () => {
    if (!input) return;
    setQrUrl(`${API_BASE}/identity/${input.toUpperCase()}/qr`);
  };

  return (
    <section className="panel" style={{ maxWidth: '600px', margin: '0 auto' }}>
      <h2>{tr(t, "scanQrTitle", "Scan QR / Open SwasthyaID")}</h2>
      <p>{tr(t, "scanQrDescription", "Enter a Swasthya ID (e.g. SW-100001) to view worker history or generate a pass.")}</p>
      
      <div className="inline-form" style={{ marginTop: '20px', gap: '8px', display: 'flex' }}>
        <input
          value={input}
          onChange={(event) => {
             setInput(event.target.value.toUpperCase());
             setQrUrl(""); // reset image when typing
          }}
          placeholder="SW-XXXXXX"
          style={{ flex: 1, padding: '10px' }}
        />
        <button type="button" onClick={() => navigate(`/worker/${encodeURIComponent(input)}`)} disabled={!input}>
          {tr(t, "openRecord", "Open Record")}
        </button>
        <button type="button" onClick={handleGenerate} disabled={!input} style={{ backgroundColor: '#10b981', color: '#fff' }}>
          {tr(t, "generateQr", "Generate QR")}
        </button>
      </div>

      {qrUrl && (
        <div style={{ marginTop: '30px', textAlign: 'center', padding: '20px', background: '#f9fafb', borderRadius: '8px', border: '1px solid #e5e7eb' }}>
          <h3 style={{ margin: '0 0 15px 0', fontSize: '1.2rem', color: '#374151' }}>{tr(t, "workerPass", "Worker Pass")}: {input}</h3>
          <img src={qrUrl} alt={`QR Code for ${input}`} style={{ maxWidth: '250px', border: '1px solid #ddd', padding: '10px', background: 'white' }} />
          <p style={{ marginTop: '10px', fontSize: '14px', color: '#6b7280' }}>{tr(t, "scanThisCode", "Scan this code locally or on a mobile device.")}</p>
        </div>
      )}
    </section>
  );
}
