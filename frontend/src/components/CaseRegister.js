import React from 'react';
import { useForensic } from '../context/ForensicContext';

function CaseRegister() {
  const { casesList, loadingCases, fetchCases, openCase, setPage } = useForensic();

  return (
    <div className="panel table">
      <div className="panel-head" style={{display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "15px"}}>
        <div>
          <span className="eyebrow">CASE REGISTER</span>
          <h3 style={{margin: "4px 0 0 0"}}>Forensic investigations ({casesList.length})</h3>
        </div>
        <div style={{display: "flex", gap: "8px"}}>
          <button 
            type="button" 
            onClick={fetchCases} 
            disabled={loadingCases}
            style={{padding: "8px 12px", fontSize: "10px"}}
          >
            {loadingCases ? "REFRESHING..." : "↻ REFRESH"}
          </button>
          <button 
            type="button" 
            onClick={() => setPage("command")}
            style={{padding: "8px 12px", fontSize: "10px"}}
          >
            + NEW CASE
          </button>
        </div>
      </div>

      {loadingCases ? (
        <div className="empty">Fetching forensic case history from database...</div>
      ) : casesList && casesList.length > 0 ? (
        <div className="case-list-grid" style={{display: "flex", flexDirection: "column", gap: "10px"}}>
          {casesList.map((c, idx) => {
            const caseId = c.case_id || c.id || `CASE-${idx}`;
            const risk = c.risk_score ?? 0;
            const label = c.risk_label || (risk > 80 ? "CRITICAL" : risk > 60 ? "HIGH" : risk > 40 ? "MODERATE" : "LOW");
            const dateStr = c.timestamp ? new Date(c.timestamp).toLocaleString() : "Recently";
            
            return (
              <div 
                className="case-card" 
                key={caseId} 
                onClick={() => openCase(c)}
                style={{cursor: "pointer", transition: "all 0.2s ease"}}
                title="Click to review complete forensic findings & risk analysis"
              >
                <b>{caseId}</b>
                <span style={{overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap"}}>
                  {c.url}
                </span>
                <strong>{risk}/100 {label}</strong>
                <small>{dateStr}</small>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="empty">
          No cases recorded in database yet. Start an investigation from the Command Center to record forensic evidence.
        </div>
      )}
    </div>
  );
}

export default CaseRegister;
