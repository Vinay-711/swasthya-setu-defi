import { useState } from "react";

import { api } from "../services/api";
import { tr } from "../services/i18n";

export default function WorkerTrackingPage({ t }) {
  const [workerId, setWorkerId] = useState("");
  const [state, setState] = useState("Maharashtra");
  const [city, setCity] = useState("Mumbai");
  const [latitude, setLatitude] = useState("");
  const [longitude, setLongitude] = useState("");
  const [timeline, setTimeline] = useState([]);
  const [error, setError] = useState("");

  async function submit(event) {
    event.preventDefault();
    setError("");
    try {
      await api.updateLocation({ worker_id: workerId, state, city, latitude: latitude || null, longitude: longitude || null });
      const history = await api.listLocations(workerId);
      setTimeline(history);
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  return (
    <section className="grid-2">
      <article className="panel">
        <h2>{tr(t, "sehatsetuLocationSync", "SehatSetu Location Sync")}</h2>
        <form className="stack-form" onSubmit={submit}>
          <label>{tr(t, "workerId", "Worker ID")}</label>
          <input value={workerId} onChange={(event) => setWorkerId(event.target.value)} required />

          <label>{tr(t, "state", "State")}</label>
          <input value={state} onChange={(event) => setState(event.target.value)} required />

          <label>{tr(t, "city", "City")}</label>
          <input value={city} onChange={(event) => setCity(event.target.value)} required />

          <label>{tr(t, "latitude", "Latitude")}</label>
          <input value={latitude} onChange={(event) => setLatitude(event.target.value)} placeholder="19.0760" />

          <label>{tr(t, "longitude", "Longitude")}</label>
          <input value={longitude} onChange={(event) => setLongitude(event.target.value)} placeholder="72.8777" />

          <button type="submit">{tr(t, "saveLocation", "Save Location")}</button>
        </form>
        {error ? <p className="error-text">{error}</p> : null}
      </article>

      <article className="panel">
        <h2>{tr(t, "locationTimeline", "Location Timeline")}</h2>
        {!timeline.length ? (
          <p>{tr(t, "noMovementEntries", "No movement entries yet.")}</p>
        ) : (
          <ul className="timeline-list">
            {timeline.map((item) => (
              <li key={item.id}>
                <strong>{item.city}, {item.state}</strong>
                <span>{new Date(item.created_at).toLocaleString()}</span>
              </li>
            ))}
          </ul>
        )}
      </article>
    </section>
  );
}
