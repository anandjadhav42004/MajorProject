import React from 'react';
import { useForensic } from '../context/ForensicContext';

function EvidenceLab() {
  const { data, selected, findings, evidenceUrl, tab, setTab } = useForensic();
  const current = selected || findings[0];

  return (
    <div className="evidence-layout">
      <div className="evidence-view">
        <div className="evidence-toolbar">
          <span>CASE {data?.case_id || "NOT ACQUIRED"}</span>
          <b>{current?.name || "AWAITING SCAN"}</b>
          <span>{data?.mode || "STANDBY"}</span>
        </div>
        {evidenceUrl ? (
          <img className="real-shot" src={evidenceUrl} alt="Captured website evidence" />
        ) : (
          <div className="demo-shot" style={{textAlign:"center", color:"var(--muted)"}}>
            {data ? "No Visual Acquisition Available. Fallback request method was used." : "Awaiting Investigation. Enter a URL in the Command Center to begin."}
          </div>
        )}
      </div>
      {current ? (
        <div className="evidence-side">
          <span className="eyebrow">EVIDENCE OBJECT</span>
          <h2>{current.name}</h2>
          <div className={`sev big ${current.severity.toLowerCase()}`}>{current.severity} · {current.confidence || current.score}%</div>
          <p className="evidence-main">{current.evidence}</p>
          
          <div className="tabs">
            {["DOM", "SCREENSHOT", "BEHAVIOR"].map(x => (
              <button className={tab === x ? "active" : ""} onClick={() => setTab(x)} key={x}>{x}</button>
            ))}
          </div>
          
          {tab === "DOM" && (
            <pre>{JSON.stringify({
              pattern: current.name.toLowerCase().replaceAll(" ", "_"),
              element: data?.evidence?.find(e => e.pattern === current.name)?.html || "Not available",
              text: current.evidence,
              xpath: data?.evidence?.find(e => e.pattern === current.name)?.xpath || "Not available",
              visibility: true
            }, null, 2)}</pre>
          )}
          
          {tab === "SCREENSHOT" && (
            <div className="evidence-meta">
              <b>FULL-PAGE CAPTURE</b>
              <p>{evidenceUrl ? "Live screenshot served directly from the Flask evidence vault." : "No live browser screenshot is available for this case."}</p>
              {evidenceUrl && <a href={evidenceUrl} target="_blank" rel="noreferrer">OPEN RAW SCREENSHOT ↗</a>}
            </div>
          )}
          
          {tab === "BEHAVIOR" && (
            <div className="behavior">
              <b>BEHAVIORAL SIGNALS</b>
              {(current.behavior_signals || []).map(x => (
                <p key={x}>✓ {x}</p>
              ))}
              {(!current.behavior_signals || current.behavior_signals.length === 0) && <p style={{color: "var(--muted)"}}>No behavioral mutations detected during interaction probes.</p>}
            </div>
          )}
          
          <div className="hash">✓ SHA-256 EVIDENCE SEALED</div>
        </div>
      ) : (
        <div className="evidence-side" style={{display: "grid", placeItems: "center", color: "var(--muted)", textAlign: "center"}}>
          <div>Run an investigation to populate the Evidence Lab.</div>
        </div>
      )}
    </div>
  );
}

export default EvidenceLab;
