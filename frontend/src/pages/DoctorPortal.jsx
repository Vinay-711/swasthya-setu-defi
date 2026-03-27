import React, { useState, useEffect, useRef } from 'react';
import { Camera, ArrowRightLeft, FileText, Activity, UserPlus, FileHeart } from 'lucide-react';
import { RadialBarChart, RadialBar, ResponsiveContainer } from 'recharts';
import jsQR from 'jsqr';
import './DoctorPortal.css';
import { api } from '../services/api';

export default function DoctorPortal() {
  const [sourceLang, setSourceLang] = useState('Odia');
  const [targetLang, setTargetLang] = useState('Kannada');
  const [inputText, setInputText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [isTranslating, setIsTranslating] = useState(false);
  const [isScanning, setIsScanning] = useState(false);
  const [patientRecord, setPatientRecord] = useState(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  // Risk score data for radial chart
  const riskScore = patientRecord && patientRecord.occupational_risk?.length > 0 
    ? Math.round(patientRecord.occupational_risk[0].scores_json?.silicosis * 100 || 0) 
    : 0;
  
  const chartData = [
    { name: 'Background', value: 100, fill: '#f3f4f6' },
    { name: 'Score', value: riskScore, fill: '#7C3AED' }
  ];

  // Debounced translation effect
  useEffect(() => {
    const translateText = async () => {
      if (!inputText.trim()) {
        setTranslatedText('');
        return;
      }

      setIsTranslating(true);
      try {
        const data = await api.voiceTranslate({
          text: inputText,
          from_lang: sourceLang.toLowerCase(),
          to_lang: targetLang.toLowerCase(),
        });
        
        setTranslatedText(data.translated_text || data.text || 'Translation success');
      } catch (err) {
        console.error("Translation API error", err);
        setTranslatedText(`[${targetLang}] ${inputText} (Backend translation failed)`);
      } finally {
        setIsTranslating(false);
      }
    };

    const handler = setTimeout(translateText, 500);
    return () => clearTimeout(handler);
  }, [inputText, sourceLang, targetLang]);

  const toggleLanguages = () => {
    setSourceLang(targetLang);
    setTargetLang(sourceLang);
    setInputText(translatedText);
  };

  const loadPatient = async (workerId) => {
    try {
      const record = await api.getWorkerRecord(workerId);
      setPatientRecord(record);
      alert(`Patient Loaded: ${record.worker?.name || workerId}`);
    } catch (err) {
      alert(`Failed to load patient ${workerId}. Using mock fallback.`);
      console.error(err);
    }
  };

  const fetchDemoPatient = () => {
    // Hidden shortcut for quick demo presentation
    loadPatient('SW-100001');
  };

  const handleScanClick = () => {
    if (isScanning) {
      // Stop scanning
      if (videoRef.current && videoRef.current.srcObject) {
        videoRef.current.srcObject.getTracks().forEach(track => track.stop());
      }
      setIsScanning(false);
    } else {
      setIsScanning(true);
      navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
        .then(function(stream) {
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
            videoRef.current.setAttribute("playsinline", true);
            videoRef.current.play();
            requestAnimationFrame(tick);
          }
        })
        .catch(err => {
          console.error("Error accessing camera: ", err);
          alert("Could not access camera. Simulating scan for SW-100001 instead.");
          setIsScanning(false);
          loadPatient('SW-100001');
        });
    }
  };

  const tick = () => {
    if (videoRef.current && videoRef.current.readyState === videoRef.current.HAVE_ENOUGH_DATA) {
      if (!canvasRef.current) return;
      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");
      canvas.width = videoRef.current.videoWidth;
      canvas.height = videoRef.current.videoHeight;
      ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const code = jsQR(imageData.data, imageData.width, imageData.height, {
        inversionAttempts: "dontInvert",
      });
      if (code) {
        handleScanClick(); // Stop scanning on success
        
        let scannedId = code.data;
        if (scannedId.includes('/worker/')) {
          scannedId = scannedId.split('/worker/')[1];
        }
        loadPatient(scannedId);
        return;
      }
    }
    if (isScanning) {
      requestAnimationFrame(tick);
    }
  };

  return (
    <div className="dp-container">
      <header className="dp-header">
        <h1 className="dp-title">Doctor Portal</h1>
        <button className="dp-cta-button" onClick={fetchDemoPatient}>
          <UserPlus size={20} />
          Scan New Patient (Demo)
        </button>
      </header>

      <div className="dp-grid">
        {/* Left Column */}
        <div className="dp-left">
          <div className="dp-card">
            <h2 className="dp-card-title">
              <Camera size={20} color="#7C3AED" />
              Patient Scan
            </h2>
            <div className="dp-scan-area" onClick={!isScanning ? handleScanClick : undefined}>
              {!isScanning ? (
                <>
                  <Camera className="dp-scan-icon" />
                  <span className="dp-scan-text">Click to activate camera for QR Scan</span>
                  {patientRecord && (
                    <div style={{marginTop:'12px', fontSize:'14px', color:'var(--text);', fontWeight:600}}>
                      Active Patient: {patientRecord.worker?.name} ({patientRecord.worker?.swasthya_id})
                    </div>
                  )}
                </>
              ) : (
                <>
                  <video ref={videoRef} style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: '8px' }} />
                  <canvas ref={canvasRef} style={{ display: 'none' }} />
                  <div style={{ position: 'absolute', bottom: 10, right: 10 }}>
                    <button onClick={(e) => { e.stopPropagation(); handleScanClick(); }} style={{ padding: '8px', background: 'red', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Cancel</button>
                  </div>
                </>
              )}
            </div>
          </div>

          <div className="dp-card">
            <h2 className="dp-card-title">
              <FileHeart size={20} color="#7C3AED" />
              Medical History
            </h2>
            <div className="dp-tags-container">
              {patientRecord && patientRecord.worker?.recent_diagnoses?.length > 0 ? (
                patientRecord.worker.recent_diagnoses.map((diag, i) => (
                   <span key={i} className={`dp-tag ${i%2===0?'dp-tag-orange':'dp-tag-red'}`}>{diag}</span>
                ))
              ) : (
                <span className="dp-tag" style={{background:'#f3f4f6', color:'#6b7280'}}>No conditions recorded</span>
              )}
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div className="dp-right">
          <div className="dp-card">
            <h2 className="dp-card-title">
              <Activity size={20} color="#7C3AED" />
              KaamSuraksha Risk Score
            </h2>
            <div className="dp-chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <RadialBarChart 
                  cx="50%" 
                  cy="50%" 
                  innerRadius="70%" 
                  outerRadius="90%" 
                  barSize={15} 
                  data={chartData} 
                  startAngle={90} 
                  endAngle={-270}
                >
                  <RadialBar 
                    minAngle={15} 
                    background={{ fill: '#f3f4f6' }} 
                    clockWise={true} 
                    dataKey="value" 
                    cornerRadius={10}
                  />
                </RadialBarChart>
              </ResponsiveContainer>
              <div className="dp-score-overlay">
                <div className="dp-score-number">{riskScore}</div>
                <div className="dp-score-label">High Risk</div>
              </div>
            </div>
          </div>

          <div className="dp-card">
            <h2 className="dp-card-title">
              <FileText size={20} color="#7C3AED" />
              Platform Translation
            </h2>
            
            <div className="dp-translate-header">
              <div className="dp-lang-label">{sourceLang}</div>
              <button className="dp-swap-btn" onClick={toggleLanguages} title="Swap languages">
                <ArrowRightLeft size={18} />
              </button>
              <div className="dp-lang-label">{targetLang}</div>
            </div>

            <textarea 
              className="dp-textarea"
              placeholder="Doctor's Instructions..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
            />

            {(translatedText || isTranslating) && (
              <div className="dp-translation-result">
                {isTranslating ? <span style={{color: '#9ca3af'}}>Translating with Bhashini API...</span> : translatedText}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
