import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { api } from "../services/api";
import { tr } from "../services/i18n";

export default function DashboardPage({ t }) {
  const [healthStatus, setHealthStatus] = useState("checking");
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    api.health()
      .then((res) => setHealthStatus(res.status))
      .catch(() => setHealthStatus("down"));

    api.me()
      .then((res) => setProfile(res))
      .catch(() => setProfile(null));
  }, []);

  return (
    <section className="grid-2">
      <article className="panel">
        <h2>{tr(t, "systemStatus", "System Status")}</h2>
        <p>{tr(t, "apiHealth", "API health")}: {healthStatus}</p>
        {profile ? (
          <>
            <p>{tr(t, "loggedInAs", "Logged in as")}: {profile.name}</p>
            <p>{tr(t, "role", "Role")}: {profile.role}</p>
            <p>{tr(t, "swasthyaId", "Swasthya ID")}: {profile.swasthya_id || tr(t, "notGenerated", "Not generated")}</p>
          </>
        ) : (
          <p>{tr(t, "profileFetchError", "Unable to fetch user profile.")}</p>
        )}
      </article>

      <article className="panel">
        <h2>{tr(t, "quickActions", "Quick Actions")}</h2>
        <ul className="action-list">
          <li>
            <Link to="/risk-analysis">{tr(t, "runRiskAssessment", "Run KaamSuraksha Risk Assessment")}</Link>
          </li>
          <li>
            <Link to="/voice-demo">{tr(t, "openVoiceDemo", "Open Voice Input Demo")}</Link>
          </li>
          <li>
            <Link to="/upload-documents">{tr(t, "uploadMedicalDocument", "Upload Medical Document")}</Link>
          </li>
          <li>
            <Link to="/scan-qr">{tr(t, "openWorkerRecordByQr", "Open Worker Record by QR ID")}</Link>
          </li>
          <li>
            <Link to="/worker-tracking">{tr(t, "updateWorkerLocation", "Update Worker Location")}</Link>
          </li>
        </ul>
      </article>
    </section>
  );
}
