import React from 'react';
import { useForensic } from '../context/ForensicContext';

function CaseRegister() {
  const { data, setPage } = useForensic();

  return (
    <div className="panel table">
      <div className="panel-head">
        <div>
          <span className="eyebrow">CASE REGISTER</span>
          <h3>Forensic investigations</h3>
        </div>
        <button onClick={() => setPage("scan")}>NEW CASE</button>
      </div>
      {data ? (
        <div className="case-card">
          <b>{data.case_id}</b>
          <span>{data.url}</span>
          <strong>{data.risk_score}/100 {data.risk_label}</strong>
          <small>{data.timestamp}</small>
        </div>
      ) : (
        <div className="empty">No live cases yet. Start an investigation to create a case with screenshot, DOM and risk evidence.</div>
      )}
    </div>
  );
}

export default CaseRegister;
