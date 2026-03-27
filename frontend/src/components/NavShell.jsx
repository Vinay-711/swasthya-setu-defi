import { Link, Outlet, useLocation, useNavigate } from "react-router-dom";

import { clearToken } from "../services/api";

export default function NavShell({ t, language, setLanguage, mockMode, onToggleMockMode }) {
  const location = useLocation();
  const navigate = useNavigate();

  const navItems = [
    { to: "/dashboard", label: t.dashboard },
    { to: "/risk-analysis", label: t.risk },
    { to: "/voice-demo", label: t.voiceDemo },
    { to: "/scan-qr", label: t.scanQr },
    { to: "/upload-documents", label: t.uploadDocs },
    { to: "/worker-tracking", label: t.tracking },
  ];

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">{t.appName}</div>
        <nav>
          {navItems.map((item) => (
            <Link
              key={item.to}
              className={`nav-link ${location.pathname.startsWith(item.to) ? "active" : ""}`}
              to={item.to}
            >
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="toolbar">
          <button className="ghost-btn" onClick={onToggleMockMode} type="button">
            {mockMode ? t.mockOn : t.mockOff}
          </button>
          <label htmlFor="lang-select">{t.language}</label>
          <select
            id="lang-select"
            value={language}
            onChange={(event) => setLanguage(event.target.value)}
          >
            <option value="en">EN</option>
            <option value="hi">HI</option>
          </select>
          <button
            className="ghost-btn"
            onClick={() => {
              clearToken();
              navigate("/login", { replace: true });
            }}
            type="button"
          >
            {t.logout}
          </button>
        </div>
      </header>
      <main className="content-wrap">
        <Outlet />
      </main>
    </div>
  );
}
