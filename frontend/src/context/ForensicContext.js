import React, { createContext, useState, useEffect, useContext } from 'react';

const ForensicContext = createContext();

export const useForensic = () => useContext(ForensicContext);

const API = process.env.REACT_APP_API_URL || "http://localhost:5001";



export const ForensicProvider = ({ children }) => {
  const [intro, setIntro] = useState(true);
  const [theme, setTheme] = useState(localStorage.getItem("afd-theme") || "dark");
  const [page, setPage] = useState("command");
  const [url, setUrl] = useState("https://example.com/product/123");
  const [data, setData] = useState(null);
  const [selected, setSelected] = useState(null);
  const [tab, setTab] = useState("DOM");
  const [toast, setToast] = useState("");

  const findings = data?.patterns || [];
  const risk = data?.risk_score ?? 0;

  useEffect(() => {
    document.body.dataset.theme = theme;
    localStorage.setItem("afd-theme", theme);
  }, [theme]);

  useEffect(() => {
    const t = setTimeout(() => setIntro(false), 4200);
    return () => clearTimeout(t);
  }, []);

  const notify = (msg, duration = 3000) => {
    setToast(msg);
    setTimeout(() => setToast(""), duration);
  };

  const scan = async () => {
    setPage("scan");
    try {
      const r = await fetch(`${API}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url })
      });
      if (!r.ok) {
        const err = await r.json().catch(() => ({}));
        throw new Error(err.error || `Server Error (${r.status})`);
      }
      const d = await r.json();
      setData(d);
      setSelected(d.patterns?.[0] || null);
      notify("Live forensic evidence captured and sealed");
      setTimeout(() => setPage("result"), 700);
    } catch (e) {
      setData(null);
      notify(`⚠️ ${e.message}`, 6000);
      setTimeout(() => setPage("command"), 1200);
    }
  };

  const download = async () => {
    if (!data) {
      notify("Run an investigation first");
      return;
    }
    try {
      const r = await fetch(`${API}/reports/${data.case_id}/download`);
      if (!r.ok) throw new Error();
      const blob = await r.blob();
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = `${data.case_id}_forensic_report.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(a.href);
      notify("Forensic report downloaded");
    } catch {
      notify("Report download failed — start the Flask backend");
    }
  };

  const evidenceUrl = data ? `${API}/evidence/${data.case_id}/screenshot` : null;

  const value = {
    intro, setIntro,
    theme, setTheme,
    page, setPage,
    url, setUrl,
    data, setData,
    selected, setSelected,
    tab, setTab,
    toast, setToast,
    findings, risk,
    notify, scan, download,
    evidenceUrl, API
  };

  return (
    <ForensicContext.Provider value={value}>
      {children}
    </ForensicContext.Provider>
  );
};
