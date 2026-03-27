import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { api, setToken } from "../services/api";

const ROLES = ["worker", "employer", "govt", "clinic"];

export default function LoginRegisterPage({ t }) {
  const navigate = useNavigate();
  const [mode, setMode] = useState("login");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    email: "",
    password: "",
    role: "worker",
    name: "",
    phone: "",
    language: "en",
  });

  async function submit(event) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response =
        mode === "login"
          ? await api.login({ email: form.email, password: form.password })
          : await api.register(form);
      setToken(response.access_token);
      navigate("/dashboard", { replace: true });
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="auth-shell">
      <section className="auth-card">
        <h1>{t.appName}</h1>
        <div className="auth-toggle">
          <button className={mode === "login" ? "active" : ""} onClick={() => setMode("login")} type="button">
            {t.login}
          </button>
          <button
            className={mode === "register" ? "active" : ""}
            onClick={() => setMode("register")}
            type="button"
          >
            {t.register}
          </button>
        </div>

        <form onSubmit={submit} className="auth-form">
          {mode === "register" ? (
            <>
              <label>{t.name}</label>
              <input value={form.name} onChange={(e) => setForm((prev) => ({ ...prev, name: e.target.value }))} required />

              <label>{t.phone}</label>
              <input value={form.phone} onChange={(e) => setForm((prev) => ({ ...prev, phone: e.target.value }))} required />

              <label>{t.role}</label>
              <select value={form.role} onChange={(e) => setForm((prev) => ({ ...prev, role: e.target.value }))}>
                {ROLES.map((role) => (
                  <option key={role} value={role}>
                    {role}
                  </option>
                ))}
              </select>
            </>
          ) : null}

          <label>{t.email}</label>
          <input
            type="email"
            value={form.email}
            onChange={(e) => setForm((prev) => ({ ...prev, email: e.target.value }))}
            required
          />

          <label>{t.password}</label>
          <input
            type="password"
            value={form.password}
            onChange={(e) => setForm((prev) => ({ ...prev, password: e.target.value }))}
            required
          />

          {error ? <p className="error-text">{error}</p> : null}
          <button type="submit" disabled={loading}>
            {loading ? t.pleaseWait : mode === "login" ? t.login : t.register}
          </button>
        </form>
      </section>
    </main>
  );
}
