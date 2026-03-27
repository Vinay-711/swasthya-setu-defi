import React, { useState, useEffect, useRef } from 'react';
import QRCode from 'qrcode';
import { Mic, QrCode as QrIcon, FileText, Home, User, Settings } from 'lucide-react';
import './MobileAppHome.css';

export default function MobileAppHome({ workerId = "WKR-90210-XYZ" }) {
  const [isRecording, setIsRecording] = useState(false);
  const [recordedAudio, setRecordedAudio] = useState(null);
  const canvasRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  useEffect(() => {
    if (canvasRef.current && workerId) {
      QRCode.toCanvas(canvasRef.current, workerId, {
        width: 150,
        margin: 2,
        color: {
          dark: '#E5681A', // Orange QR code
          light: '#FFF7ED' // Light orange bg
        }
      }, (error) => {
        if (error) console.error("QR Code Error:", error);
      });
    }
  }, [workerId]);

  const toggleRecording = async () => {
    if (isRecording) {
      // Stop recording
      if (mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive") {
        mediaRecorderRef.current.stop();
        mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      }
      setIsRecording(false);
    } else {
      // Start recording
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorderRef.current = new MediaRecorder(stream);
        chunksRef.current = [];

        mediaRecorderRef.current.ondataavailable = (e) => {
          if (e.data.size > 0) chunksRef.current.push(e.data);
        };

        mediaRecorderRef.current.onstop = () => {
          const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
          const url = URL.createObjectURL(blob);
          setRecordedAudio(url);
        };

        mediaRecorderRef.current.start();
        setIsRecording(true);
        setRecordedAudio(null);
      } catch (err) {
        console.error("Microphone access denied or failed", err);
        alert("Microphone access is required for voice input.");
      }
    }
  };

  return (
    <div className="mobile-home-wrapper">
      <div className="mobile-phone-frame">
        {/* Header */}
        <header className="mobile-header">
          <div className="mobile-header-btn">
            SwasthyaSetu
          </div>
        </header>

        {/* Content */}
        <div className="mobile-content">
          
          {/* QR Code Section */}
          <section className="mobile-section">
            <h3 className="mobile-section-title">
              <QrIcon size={20} color="#E5681A" />
              My QR Code / ID
            </h3>
            <div className="qr-container">
              <canvas ref={canvasRef} className="canvas-qr" />
            </div>
            <p style={{ textAlign: 'center', marginTop: '12px', color: '#6b7280', fontSize: '14px', fontWeight: 500 }}>
              {workerId}
            </p>
          </section>

          {/* Voice Input Section */}
          <section className="mobile-section">
            <h3 className="mobile-section-title">
              <Mic size={20} color="#2563EB" />
              Voice Input
            </h3>
            <div className="voice-input-container">
              <button 
                className={`mic-btn ${isRecording ? 'recording' : ''}`}
                onClick={toggleRecording}
                aria-label={isRecording ? "Stop Recording" : "Start Recording"}
              >
                <Mic size={32} />
              </button>
              <div className="recording-status">
                {isRecording ? "Recording in progress..." : "Tap to speak symptoms"}
              </div>
              
              {recordedAudio && !isRecording && (
                <div style={{ marginTop: '12px', width: '100%' }}>
                  <audio src={recordedAudio} controls style={{ width: '100%' }} />
                </div>
              )}
            </div>
          </section>

          {/* Health Records Section */}
          <section className="mobile-section">
            <h3 className="mobile-section-title">
              <FileText size={20} color="#10b981" />
              Recent Health Records
            </h3>
            
            <div className="record-item">
              <div className="record-header">
                <span>Blood Pressure</span>
                <span style={{color: '#10b981'}}>Normal</span>
              </div>
              <div className="record-bar-bg">
                <div className="record-bar-fill" style={{ width: '85%' }}></div>
              </div>
            </div>

            <div className="record-item">
              <div className="record-header">
                <span>General Checkup</span>
                <span style={{color: '#10b981'}}>Clear</span>
              </div>
              <div className="record-bar-bg">
                <div className="record-bar-fill" style={{ width: '100%' }}></div>
              </div>
            </div>
          </section>

        </div>

        {/* Bottom Nav Mockup */}
        <nav className="mobile-nav">
          <div className="nav-item active">
            <Home size={24} />
          </div>
          <div className="nav-item">
            <User size={24} />
          </div>
          <div className="nav-item">
            <Settings size={24} />
          </div>
        </nav>
      </div>
    </div>
  );
}
