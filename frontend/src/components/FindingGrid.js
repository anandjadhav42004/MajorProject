import React from 'react';
import { useForensic } from '../context/ForensicContext';

function FindingGrid() {
  const { findings, setSelected, setPage } = useForensic();
  
  return (
    <div className="findings">
      {findings.map(f => (
        <button 
          className="finding" 
          onClick={() => { setSelected(f); setPage("evidence"); }} 
          key={f.name}
        >
          <div>
            <span className={`sev ${f.severity.toLowerCase()}`}>{f.severity}</span>
            <b>{f.score}%</b>
          </div>
          <h4>{f.name}</h4>
          <p>{f.evidence}</p>
          <small>{f.type}</small>
        </button>
      ))}
    </div>
  );
}

export default FindingGrid;
