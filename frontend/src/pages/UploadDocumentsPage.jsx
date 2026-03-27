import { useState } from "react";

import { api } from "../services/api";
import { tr } from "../services/i18n";

export default function UploadDocumentsPage({ t }) {
  const [workerId, setWorkerId] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleUpload(event) {
    event.preventDefault();
    if (!workerId || !file) return;

    setLoading(true);
    setError("");
    try {
      const response = await api.uploadDocument(workerId, file);
      setResult(response);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="panel">
      <h2>{tr(t, "documentUploadTitle", "Document AI Upload")}</h2>
      <form onSubmit={handleUpload} className="stack-form">
        <label>{tr(t, "workerId", "Worker ID")}</label>
        <input value={workerId} onChange={(event) => setWorkerId(event.target.value)} required />

        <label>{tr(t, "documentFile", "Document File")}</label>
        <input type="file" onChange={(event) => setFile(event.target.files?.[0] || null)} required />

        <button type="submit" disabled={loading || !workerId || !file}>
          {loading ? tr(t, "uploading", "Uploading...") : tr(t, "uploadAndProcess", "Upload & Process")}
        </button>
      </form>

      {error ? <p className="error-text">{error}</p> : null}

      {result ? (
        <article className="json-card">
          <h3>{tr(t, "parsedOutput", "Parsed Output")}</h3>
          <pre>{JSON.stringify(result.parsed_json, null, 2)}</pre>
        </article>
      ) : null}
    </section>
  );
}
