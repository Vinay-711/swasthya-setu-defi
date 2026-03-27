import { useEffect, useMemo, useState } from "react";

import { tr } from "../services/i18n";

function getRiskClass(scorePercent) {
  if (scorePercent > 70) return "risk-red";
  if (scorePercent > 40) return "risk-amber";
  return "risk-green";
}

export default function RiskScoreCard({ t, score = 0, riskLevel = "LOW", predictedDisease = "-" }) {
  const finalPercent = useMemo(() => Math.round(score * 100), [score]);
  const [animated, setAnimated] = useState(0);

  useEffect(() => {
    const start = performance.now();
    const duration = 1000;
    let frame;

    const step = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      setAnimated(Math.round(finalPercent * progress));
      if (progress < 1) frame = requestAnimationFrame(step);
    };

    setAnimated(0);
    frame = requestAnimationFrame(step);
    return () => cancelAnimationFrame(frame);
  }, [finalPercent]);

  return (
    <section className={`score-card ${getRiskClass(animated)}`}>
      <h3>{tr(t, "predictedRisk", "Predicted Occupational Risk")}</h3>
      <div className="score-number">{animated}%</div>
      <p>{tr(t, "riskLevel", "Risk level")}: {riskLevel}</p>
      <p>{tr(t, "likelyDisease", "Likely disease")}: {predictedDisease}</p>
    </section>
  );
}
