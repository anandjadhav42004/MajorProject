import React from "react";
import "./App.css";
import { ForensicProvider, useForensic } from "./context/ForensicContext";
import CommandCenter from "./components/CommandCenter";
import Scanner from "./components/Scanner";
import Result from "./components/Result";
import CaseRegister from "./components/CaseRegister";
import EvidenceLab from "./components/EvidenceLab";
import RiskAnalytics from "./components/RiskAnalytics";
import ReportDashboard from "./components/ReportDashboard";

function AppContent() {
  const API = process.env.REACT_APP_API_URL || "http://127.0.0.1:5001";
  const { intro, setIntro, theme, setTheme, page, setPage, toast } = useForensic();

  if (intro) {
    return (
      <div className="intro welcome-screen">
        <div className="intro-grid" />
        <div className="welcome-noise" />
        <div className="intro-core">
          <div className="welcome-art" aria-hidden="true">
            <div className="art-halo" />
            <div className="aperture aperture-back" />
            <div className="aperture aperture-front" />
            <div className="aperture-core"><span>DL</span><i /></div>
            <div className="art-scan" />
          </div>
          <p className="eyebrow">AUTOMATED FORENSIC INTELLIGENCE</p>
          <h1><span>WELCOME TO</span> DARKLENS</h1>
          <div className="intro-line" />
          <p>See the signals hiding in plain sight.</p>
          <button onClick={() => setIntro(false)}>ENTER FORENSIC CONSOLE <b>→</b></button>
        </div>
        <div className="intro-foot">
          <span>01</span> INITIALIZING AI ENGINE <i /> <span>02</span> BROWSER AGENT <i /> <span>03</span> EVIDENCE VAULT
        </div>
      </div>
    );
  }

  const nav = [
    ["command", "◈", "Command Center"],
    ["scan", "◎", "New Investigation"],
    ["cases", "◌", "Case Management"],
    ["evidence", "◇", "Evidence Lab"],
    ["analytics", "◒", "Risk Analytics"],
    ["reports", "▣", "Forensic Report"]
  ];

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brandmark">DL</div>
          <div><b>DARKLENS</b><span>FORENSIC OS / v3.0</span></div>
        </div>
        <nav>
          {nav.map(n => (
            <button className={page === n[0] ? "active" : ""} onClick={() => setPage(n[0])} key={n[0]}>
              <i>{n[1]}</i>{n[2]}
            </button>
          ))}
        </nav>
        <div className="systems">
          <label>SYSTEMS</label>
          <div><em />AI ENGINE <b>LIVE</b></div>
          <div><em />BROWSER <b>LIVE</b></div>
          <div><em />EVIDENCE <b>READY</b></div>
        </div>
        <button className="theme" onClick={() => setTheme(theme === "dark" ? "light" : "dark")}>
          ☼ {theme === "dark" ? "LIGHT MODE" : "DARK MODE"}
        </button>
      </aside>
      <main>
        <header>
          <div>
            <span className="eyebrow">FORENSIC INTELLIGENCE PLATFORM</span>
            <h1>{nav.find(x => x[0] === page)?.[2] || "Investigation Result"}</h1>
          </div>
          <div className="status"><span /> SYSTEM OPERATIONAL</div>
        </header>
        <div className="content">
          {page === "command" && <CommandCenter />}
          {page === "scan" && <Scanner />}
          {page === "result" && <Result />}
          {page === "cases" && <CaseRegister />}
          {page === "evidence" && <EvidenceLab />}
          {page === "analytics" && <RiskAnalytics />}
          {page === "reports" && <ReportDashboard />}
        </div>
      </main>
      {toast && <div className="toast">✓ {toast}</div>}
    </div>
  );
}

function App() {
  return (
    <ForensicProvider>
      <AppContent />
    </ForensicProvider>
  );
}

export default App;
