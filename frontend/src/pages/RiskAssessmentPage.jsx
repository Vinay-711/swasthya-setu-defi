import { useState } from "react";

import RiskScoreCard from "../components/RiskScoreCard";
import ScreeningList from "../components/ScreeningList";
import ShapExplainer from "../components/ShapExplainer";
import WorkerRiskForm from "../components/WorkerRiskForm";
import { api } from "../services/api";

const EMPTY_RESULT = {
  silicosis: 0,
  byssinosis: 0,
  occupational_asthma: 0,
  risk_level: "LOW",
  predicted_disease: "-",
  top_factors: [],
  recommendations: [],
};

export default function RiskAssessmentPage({ t }) {
  const [result, setResult] = useState(EMPTY_RESULT);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(payload) {
    setLoading(true);
    setError("");
    try {
      const response = await api.submitRiskProfile(payload);
      setResult(response);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="risk-layout">
      <WorkerRiskForm t={t} onSubmit={onSubmit} isSubmitting={loading} />

      <div className="risk-output">
        {error ? <p className="error-text">{error}</p> : null}
        <RiskScoreCard
          t={t}
          score={result.silicosis}
          riskLevel={result.risk_level}
          predictedDisease={result.predicted_disease}
        />
        <ShapExplainer t={t} factors={result.top_factors} />
        <ScreeningList t={t} recommendations={result.recommendations} />
      </div>
    </section>
  );
}
