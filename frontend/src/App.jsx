import { useMemo, useState } from "react";
import { Navigate, Route, Routes } from "react-router-dom";

import DevPanel from "./components/DevPanel";
import NavShell from "./components/NavShell";
import PortalNav from "./components/PortalNav";
import {
  ArchitecturePage,
  AshaDashboard,
  DashboardPage,
  DoctorPortal,
  EmployerPortal,
  LoginRegisterPage,
  MigrantJourneyFlow,
  MobileAppHome,
  RiskAssessmentPage,
  ScanQrPage,
  TechStackSlide,
  UploadDocumentsPage,
  VoiceDemoPage,
  WorkerRecordPage,
  WorkerTrackingPage,
} from "./pages";
import { getToken, isMockMode, setMockMode } from "./services/api";
import { I18N } from "./services/i18n";
import "./styles/app.css";

function ProtectedRoute({ children }) {
  const token = getToken();
  if (!token) return <Navigate to="/login" replace />;
  return children;
}

export default function App() {
  const [language, setLanguage] = useState("en");
  const [mockMode, setMockModeState] = useState(isMockMode());
  const [activeWorker, setActiveWorker] = useState(null);
  const t = useMemo(() => I18N[language] || I18N.en, [language]);

  const toggleMockMode = () => {
    const next = !mockMode;
    setMockMode(next);
    setMockModeState(next);
  };

  return (
    <>
    <Routes>
      <Route path="/login" element={<LoginRegisterPage t={t} />} />

      {/* Portal routes with top nav */}
      <Route element={<ProtectedRoute><PortalNav /></ProtectedRoute>}>
        <Route index element={<MobileAppHome />} />
        <Route path="/asha" element={<AshaDashboard />} />
        <Route path="/doctor" element={<DoctorPortal />} />
        <Route path="/employer" element={<EmployerPortal />} />
        <Route path="/journey" element={<MigrantJourneyFlow />} />
        <Route path="/architecture" element={<ArchitecturePage />} />
        <Route path="/tech-stack" element={<TechStackSlide />} />
      </Route>

      {/* Legacy routes with original NavShell */}
      <Route
        element={
          <ProtectedRoute>
            <NavShell
              t={t}
              language={language}
              setLanguage={setLanguage}
              mockMode={mockMode}
              onToggleMockMode={toggleMockMode}
            />
          </ProtectedRoute>
        }
      >
        <Route path="/dashboard" element={<DashboardPage t={t} />} />
        <Route path="/scan-qr" element={<ScanQrPage t={t} />} />
        <Route path="/upload-documents" element={<UploadDocumentsPage t={t} />} />
        <Route path="/risk-analysis" element={<RiskAssessmentPage t={t} />} />
        <Route path="/voice-demo" element={<VoiceDemoPage t={t} language={language} />} />
        <Route path="/worker-tracking" element={<WorkerTrackingPage t={t} />} />
        <Route path="/worker/:id" element={<WorkerRecordPage t={t} />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
    <DevPanel
      mockMode={mockMode}
      onToggleMockMode={toggleMockMode}
      activeWorker={activeWorker}
      onSelectWorker={setActiveWorker}
    />
    </>
  );
}
