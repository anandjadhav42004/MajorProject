import React from 'react';
import { useForensic } from '../context/ForensicContext';

function RiskAnalytics() {
  const { data, findings, setSelected, setPage } = useForensic();

  const dimensionExample = (k) => {
    const map = {
      manipulation_severity: "Measures how strongly the interface pushes a user toward an intended action; e.g. urgency + guilt + high-contrast CTA.",
      user_impact: "Measures likely pressure on user choice; e.g. a pre-selected add-on plus negative opt-out wording.",
      financial_risk: "Measures monetary exposure; e.g. a fee added late or an optional warranty inserted into the basket.",
      privacy_risk: "Measures consent/privacy pressure; e.g. promotional consent presented as a default.",
      deception_probability: "Measures how likely the combined signals indicate a deceptive presentation rather than a single neutral UI choice.",
      persistence: "Measures whether the suspicious behavior survives reload/session changes; e.g. a countdown resets or a default returns after refresh."
    };
    return map[k] || "Derived from correlated evidence.";
  };

  const dims = data?.dimensions || null;
  const journeySteps = data?.journey || null;

  if (!data) {
    return (
      <div className="analytics" style={{display: "grid", placeItems: "center", minHeight: "50vh", color: "var(--muted)"}}>
        <div>Awaiting investigation... No analytics available for demo state.</div>
      </div>
    );
  }

  return (
    <>
      <div className="analytics">
        <div className="panel">
          <span className="eyebrow">RISK DIMENSIONS</span>
          <h3>What each score actually means</h3>
          {Object.entries(dims).map(([k, v]) => (
            <div className="metric" key={k}>
              <div>
                <b>{k.replaceAll("_", " ")}</b>
                <strong>{v}</strong>
              </div>
              <i><em style={{ width: v + "%" }} /></i>
              <p>{dimensionExample(k)}</p>
            </div>
          ))}
        </div>
        <div className="panel">
          <span className="eyebrow">PATTERN INTELLIGENCE</span>
          <h3>Six precise detections</h3>
          <div className="analytic-list">
            {findings.map(f => (
              <button key={f.name} onClick={() => { setSelected(f); setPage("evidence"); }}>
                <span className={`sev ${f.severity.toLowerCase()}`}>{f.severity}</span>
                <div>
                  <b>{f.name}</b>
                  <p>{f.evidence}</p>
                  <small>{(f.explanation || []).join(" • ")}</small>
                </div>
                <strong>{f.score}</strong>
              </button>
            ))}
          </div>
        </div>
      </div>
      <div className="panel journey">
        <span className="eyebrow">CHECKOUT FORENSICS</span>
        <h3>Website journey risk</h3>
        <div className="journey">
          {journeySteps.map(j => (
            <div key={j.stage}>
              <b>{j.stage}</b>
              <span>{j.risk}</span>
              <p>{j.detail}</p>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default RiskAnalytics;
