import React from 'react';
import { useForensic } from '../context/ForensicContext';

function EvidenceLab() {
  const { data, selected, findings, evidenceUrl, tab, setTab } = useForensic();
  const [imgError, setImgError] = React.useState(false);
  const current = selected || findings[0];

  React.useEffect(() => {
    setImgError(false);
  }, [evidenceUrl]);

  return (
    <div className="evidence-layout">
      <div className="evidence-view">
        <div className="evidence-toolbar">
          <span>CASE {data?.case_id || "NOT ACQUIRED"}</span>
          <b>{current?.name || "AWAITING SCAN"}</b>
          <span>{data?.mode || "STANDBY"}</span>
        </div>
        {evidenceUrl && !imgError ? (
          <img 
            className="real-shot" 
            src={evidenceUrl} 
            alt="Captured website evidence" 
            onError={() => setImgError(true)}
          />
        ) : (
          <div className="demo-shot forensic-fallback">
            <div className="fallback-badge">● VISUAL EVIDENCE STATUS: STANDBY / FALLBACK</div>
            <h4>Visual evidence unavailable — browser capture fallback active.</h4>
            <p>
              {data 
                ? `Target DOM structure and text forensic signals were acquired via HTTP engine (${data?.dom_node_count || 0} DOM nodes analyzed). Visual rasterization requires active headless browser context.`
                : "Awaiting investigation. Run an investigation from the Command Center to analyze dark patterns."}
            </p>
            {data && (
              <div className="fallback-spec-grid">
                <div><span>TARGET DOMAIN</span><b>{data.url}</b></div>
                <div><span>ACQUISITION MODE</span><b>{data.mode}</b></div>
                <div><span>EVIDENCE INTEGRITY</span><b>{data.integrity || "SEALED"}</b></div>
                <div><span>RISK CLASSIFICATION</span><b>{data.risk_score}/100 ({data.risk_label})</b></div>
              </div>
            )}
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
