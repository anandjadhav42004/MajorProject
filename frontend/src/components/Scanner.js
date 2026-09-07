import React from 'react';
import { useForensic } from '../context/ForensicContext';

function Scanner() {
  const { data, url, setPage } = useForensic();

  return (
    <div className="scan-screen">
      <div className="scanner">
        <div className="scan-grid" />
        <div className="target">AFD<div className="scan-beam" /></div>
        <strong>{data ? "100" : "SCANNING"}</strong>
      </div>
      <div className="scan-info">
        <span className="eyebrow">LIVE FORENSIC ACQUISITION</span>
        <h2>{url.replace(/^https?:\/\//, "")}</h2>
        {["Launch browser agent", "Acquire rendered page", "Extract DOM + UI signals", "Capture full-page screenshot", "Correlate multimodal patterns", "Probe persistence", "Calculate risk dimensions", "Seal evidence hashes"].map((x, i) => (
          <div className="stage" key={x}>
            <span>✓</span>{x}<b>COMPLETE</b>
          </div>
        ))}
        <button onClick={() => setPage(data ? "result" : "command")}>OPEN RESULTS →</button>
      </div>
    </div>
  );
}

export default Scanner;
