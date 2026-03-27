import { useMemo, useState } from "react";

import { tr } from "../services/i18n";

const OCCUPATIONS = [
  { value: "stone_quarry", label: "Stone Quarry" },
  { value: "construction_worker", label: "Construction" },
  { value: "sandblasting_worker", label: "Sandblasting" },
  { value: "textile_mill_worker", label: "Textile Mill" },
  { value: "garment_worker", label: "Garment Factory" },
  { value: "miner", label: "Mining" },
];

const TASK_OPTIONS = [
  "drilling",
  "stone_cutting",
  "sandblasting",
  "spinning",
  "weaving",
  "chemical_mixing",
  "fume_exposure",
];

const SYMPTOM_OPTIONS = ["persistent_cough", "breathlessness", "chest_tightness", "wheeze"];

function toggle(items, value) {
  return items.includes(value) ? items.filter((item) => item !== value) : [...items, value];
}

function labelFromSlug(value) {
  return value
    .split("_")
    .map((segment) => segment.charAt(0).toUpperCase() + segment.slice(1))
    .join(" ");
}

export default function WorkerRiskForm({ t, onSubmit, isSubmitting, defaultWorkerId = "" }) {
  const [workerId, setWorkerId] = useState(defaultWorkerId);
  const [occupation, setOccupation] = useState("stone_quarry");
  const [yearsInJob, setYearsInJob] = useState(8);
  const [tasks, setTasks] = useState(["drilling", "stone_cutting"]);
  const [ppeUsage, setPpeUsage] = useState("rarely");
  const [symptoms, setSymptoms] = useState(["persistent_cough"]);

  const canSubmit = useMemo(
    () => workerId && occupation && ppeUsage && !isSubmitting,
    [workerId, occupation, ppeUsage, isSubmitting],
  );

  const submit = (event) => {
    event.preventDefault();
    if (!canSubmit) return;
    onSubmit({
      worker_id: workerId,
      occupation,
      years_in_job: Number(yearsInJob),
      tasks,
      ppe_usage: ppeUsage,
      symptoms,
    });
  };

  return (
    <form className="risk-form" onSubmit={submit}>
      <h2>{tr(t, "riskInput", "KaamSuraksha Risk Input")}</h2>
      <label>{tr(t, "workerId", "Worker ID")}</label>
      <input
        value={workerId}
        onChange={(event) => setWorkerId(event.target.value)}
        placeholder={tr(t, "workerIdPlaceholder", "UUID worker id")}
      />

      <label>{tr(t, "occupation", "Occupation")}</label>
      <select value={occupation} onChange={(event) => setOccupation(event.target.value)}>
        {OCCUPATIONS.map((item) => (
          <option key={item.value} value={item.value}>
            {item.label}
          </option>
        ))}
      </select>

      <label>{tr(t, "yearsInJob", "Years in job")}: {yearsInJob}</label>
      <input
        type="range"
        min="0"
        max="30"
        value={yearsInJob}
        onChange={(event) => setYearsInJob(event.target.value)}
      />

      <fieldset>
        <legend>{tr(t, "tasks", "Tasks")}</legend>
        <div className="chip-grid">
          {TASK_OPTIONS.map((task) => (
            <label key={task} className="chip">
              <input
                type="checkbox"
                checked={tasks.includes(task)}
                onChange={() => setTasks((prev) => toggle(prev, task))}
              />
              <span>{labelFromSlug(task)}</span>
            </label>
          ))}
        </div>
      </fieldset>

      <label>{tr(t, "ppeUsage", "PPE Usage")}</label>
      <select value={ppeUsage} onChange={(event) => setPpeUsage(event.target.value)}>
        <option value="always">{tr(t, "always", "Always")}</option>
        <option value="sometimes">{tr(t, "sometimes", "Sometimes")}</option>
        <option value="rarely">{tr(t, "rarely", "Rarely")}</option>
        <option value="never">{tr(t, "never", "Never")}</option>
      </select>

      <fieldset>
        <legend>{tr(t, "symptoms", "Symptoms")}</legend>
        <div className="chip-grid">
          {SYMPTOM_OPTIONS.map((symptom) => (
            <label key={symptom} className="chip">
              <input
                type="checkbox"
                checked={symptoms.includes(symptom)}
                onChange={() => setSymptoms((prev) => toggle(prev, symptom))}
              />
              <span>{labelFromSlug(symptom)}</span>
            </label>
          ))}
        </div>
      </fieldset>

      <button disabled={!canSubmit} type="submit">
        {isSubmitting ? tr(t, "riskAssessing", "Assessing...") : tr(t, "assessRisk", "Assess Risk")}
      </button>
    </form>
  );
}
