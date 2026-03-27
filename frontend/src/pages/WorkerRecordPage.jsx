import { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";

import { api } from "../services/api";
import { tr } from "../services/i18n";

function formatDate(value) {
  return value ? new Date(value).toLocaleString() : "-";
}

export default function WorkerRecordPage({ t }) {
  const { id } = useParams();
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) {
      setError(tr(t, "missingWorkerId", "Missing worker id"));
      setLoading(false);
      return;
    }

    setLoading(true);
    setError("");
    api.getWorkerRecord(id)
      .then((response) => setData(response))
      .catch((requestError) => setError(requestError.message))
      .finally(() => setLoading(false));
  }, [id, t]);

  const latestRisk = useMemo(() => {
    if (!data?.occupational_risk?.length) return null;
    return data.occupational_risk[0];
  }, [data]);

  if (loading) return <section className="panel">{tr(t, "loadingWorkerRecord", "Loading worker record...")}</section>;
  if (error) return <section className="panel error-text">{error}</section>;

  return (
    <section className="grid-2">
      <article className="panel">
        <h2>{data.worker.name}</h2>
        <p>{tr(t, "swasthyaId", "Swasthya ID")}: {data.swasthya_id}</p>
        <p>{tr(t, "age", "Age")}: {data.worker.age || "-"}</p>
        <p>{tr(t, "bloodType", "Blood Type")}: {data.worker.blood_type || "-"}</p>
        <p>{tr(t, "allergies", "Allergies")}: {(data.worker.allergies || []).join(", ") || tr(t, "none", "None")}</p>
        <p>{tr(t, "currentMedications", "Current Medications")}: {(data.worker.current_medications || []).join(", ") || tr(t, "none", "None")}</p>
        <p>{tr(t, "recentDiagnoses", "Recent Diagnoses")}: {(data.worker.recent_diagnoses || []).join(", ") || tr(t, "none", "None")}</p>

        <h3>{tr(t, "kaamSurakshaRisk", "KaamSuraksha Risk")}</h3>
        {latestRisk ? (
          <>
            <p>{tr(t, "riskLevel", "Risk level")}: {latestRisk.risk_level}</p>
            <p>{tr(t, "silicosisScore", "Silicosis Score")}: {Math.round((latestRisk.scores_json?.silicosis || 0) * 100)}%</p>
          </>
        ) : (
          <p>{tr(t, "noRiskProfile", "No risk profile available.")}</p>
        )}
      </article>

      <article className="panel">
        <h2>{tr(t, "lastThreeVisits", "Last 3 Visits")}</h2>
        <ul className="timeline-list">
          {(data.health_records || []).slice(0, 3).map((record) => (
            <li key={record.id}>
              <strong>{record.record_type}</strong>
              <span>{formatDate(record.created_at)}</span>
            </li>
          ))}
        </ul>

        <h2>{tr(t, "healthTimeline", "Health Timeline")}</h2>
        <ul className="timeline-list">
          {(data.health_records || []).map((record) => (
            <li key={record.id}>
              <strong>{record.record_type}</strong>
              <span>{formatDate(record.created_at)}</span>
            </li>
          ))}
          {(data.documents || []).map((doc) => (
            <li key={doc.id}>
              <strong>{tr(t, "documentUploaded", "Document Uploaded")}</strong>
              <span>{formatDate(doc.created_at)}</span>
            </li>
          ))}
        </ul>
      </article>
    </section>
  );
}
