import React from 'react';
import { useForensic } from '../context/ForensicContext';
import FindingGrid from './FindingGrid';

function Result() {
  const { data, risk, findings, setPage } = useForensic();

  return (
    <>
      <section className="result">
        <div>
          <span className="eyebrow">INVESTIGATION COMPLETE / {data?.case_id || "AWAITING SCAN"}</span>
          <h2>{risk > 80 ? "Critical" : risk > 60 ? "High" : risk > 0 ? "Moderate" : "No"} manipulation surface detected.</h2>
          <p>{data?.summary || "No active case data. Run the backend scan against a real URL to generate live evidence."}</p>
        </div>
        <div className="score">
          <strong>{risk}</strong><small>/100</small>
          <label>{risk > 80 ? "CRITICAL" : risk > 60 ? "HIGH" : "MODERATE"}</label>
        </div>
      </section>
      
      <div className="two">
        <div className="panel">
          <span className="eyebrow">EXPLAINABLE AI</span>
          <h3>Why the engine flagged this</h3>
          {(data?.patterns || findings).slice(0, 4).map(f => (
            <div className="explain" key={f.name}>
              <b>{f.name}</b><span>{f.confidence || f.score}%</span>
              <p>{(f.explanation || []).join(" • ")}</p>
            </div>
          ))}
        </div>
        <div className="panel ai">
          <span className="eyebrow">FORENSIC SUMMARY</span>
          <h3>Evidence correlation</h3>
          <p>Each classification is connected to concrete signals rather than a naked score.</p>
          <ul>
            <li>Observed text and DOM matches</li>
            <li>Visual emphasis and element context</li>
            <li>Behavior/persistence checks when browser automation is available</li>
            <li>SHA-256 evidence sealing</li>
          </ul>
          <button onClick={() => setPage("evidence")}>OPEN EVIDENCE LAB →</button>
        </div>
      </div>
      
      <div className="section-title">
        <span className="eyebrow">DETECTIONS</span>
        <h3>Precise pattern explanations</h3>
      </div>
      <FindingGrid />
    </>
  );
}

export default Result;
