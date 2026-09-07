import React from 'react';
import { useForensic } from '../context/ForensicContext';

function ReportDashboard() {
  const { data, download } = useForensic();

  return (
    <div className="report-grid">
      <div className="panel report">
        <span className="eyebrow">DOWNLOADABLE FORENSIC REPORT</span>
        <h2>{data?.case_id || "No active case"}</h2>
        <p>The backend now generates a real PDF file using ReportLab and returns it as an attachment. It contains executive summary, findings, risk dimensions and evidence hashes.</p>
        <div className="report-sections">
          <span>01 SUMMARY</span><span>02 PATTERNS</span><span>03 EVIDENCE</span>
          <span>04 DOM</span><span>05 RISK</span><span>06 INTEGRITY</span>
        </div>
        <button onClick={download}>DOWNLOAD FORENSIC PDF ↓</button>
      </div>
      <div className="panel">
        <span className="eyebrow">EVIDENCE CHAIN</span>
        <h3>Sealed objects</h3>
        {(data?.evidence || []).map(e => (
          <div className="file" key={e.id}>
            <b>{e.id}</b>
            <span>{e.pattern}</span>
            <small>{e.hash}</small>
          </div>
        ))}
        {!data && <div className="empty">Run an investigation to populate the evidence chain.</div>}
      </div>
    </div>
  );
}

export default ReportDashboard;
