import { tr } from "../services/i18n";

export default function ScreeningList({ t, recommendations = [] }) {
  return (
    <section className="panel">
      <h3>{tr(t, "recommendedScreening", "Recommended Screening")}</h3>
      {!recommendations.length ? (
        <p>{tr(t, "runAssessmentFirst", "Run an assessment to generate actions.")}</p>
      ) : (
        <ul>
          {recommendations.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      )}
    </section>
  );
}
