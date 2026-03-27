import { tr } from "../services/i18n";

export default function ShapExplainer({ t, factors = [] }) {
  return (
    <section className="panel">
      <h3>{tr(t, "topFactors", "Top SHAP-style Factors")}</h3>
      {!factors.length ? <p>{tr(t, "noFactors", "No factors yet.")}</p> : null}
      {factors.map((factor) => (
        <article key={`${factor.feature}-${factor.value}`} className="factor-row">
          <div className="factor-head">
            <strong>{factor.feature}</strong>
            <span>{Math.round((factor.impact || 0) * 100)}%</span>
          </div>
          <div className="factor-bar-wrap">
            <div className="factor-bar" style={{ width: `${Math.round((factor.impact || 0) * 100)}%` }} />
          </div>
          <small>{factor.value}</small>
        </article>
      ))}
    </section>
  );
}
