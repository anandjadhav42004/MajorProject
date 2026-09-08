import React from 'react';
import { useForensic } from '../context/ForensicContext';
import Stat from './Stat';
import FindingGrid from './FindingGrid';

function CommandCenter() {
  const { url, setUrl, scan, risk, data, findings, isScanning } = useForensic();

  return (
    <>
      <section className="hero">
        <div className="hero-card">
          <span className="eyebrow">AI-ASSISTED INVESTIGATION</span>
          <h2>Find the manipulation <em>behind the interface.</em></h2>
          <p>Analyze text, buttons, visual hierarchy, DOM structure, pop-ups, prices and interaction behavior. Every finding becomes an evidence-backed forensic record.</p>
          <div className="scanbar">
            <input 
              value={url} 
              onChange={e => setUrl(e.target.value)} 
              placeholder="https://shop.example/product" 
              disabled={isScanning}
            />
            <button onClick={() => scan()} disabled={isScanning} style={{minWidth: "170px"}}>
              {isScanning ? "Analyzing DOM & Visuals..." : "START INVESTIGATION ↗"}
            </button>
          </div>
          
          <div className="quick-demos">
            <span className="quick-label">Quick demo — no manual URL required:</span>
            <div className="quick-btn-group">
              <button 
                type="button" 
                className="quick-btn"
                onClick={() => scan("https://books.toscrape.com")}
                disabled={isScanning}
                title="Scan realistic mock store with pricing and catalog"
              >
                ⚡ Demo Store
              </button>
              <button 
                type="button" 
                className="quick-btn"
                onClick={() => scan("https://quotes.toscrape.com")}
                disabled={isScanning}
                title="Scan quote & catalog site for urgency patterns"
              >
                ⚡ Urgency Example
              </button>
              <button 
                type="button" 
                className="quick-btn"
                onClick={() => scan("https://example.com")}
                disabled={isScanning}
                title="Scan clean baseline domain"
              >
                ⚡ Clean Site
              </button>
            </div>
          </div>

          <div className="chips">
            <span>TEXT</span><span>DOM</span><span>VISUAL</span><span>BEHAVIOR</span><span>SCREENSHOT</span><span>HASH</span>
          </div>
        </div>
        <div className="risk-card">
          <div className="risk-ring">
            <strong>{risk}</strong><small>/100</small>
          </div>
          <b>OVERALL RISK</b>
          <label>{risk > 80 ? "CRITICAL" : risk > 60 ? "HIGH" : risk > 40 ? "MODERATE" : "LOW"}</label>
        </div>
      </section>
      
      <section className="stats">
        <Stat t="ACTIVE CASE" v={data ? "01" : "00"} s={data ? "Live case loaded" : "Awaiting scan"} />
        <Stat t="PATTERNS" v={findings.length} s={data ? "Correlated findings" : "No live data"} />
        <Stat t="DOM SIGNALS" v={data?.dom_node_count ?? "—"} s="Extracted from target" />
        <Stat t="EVIDENCE" v={data?.evidence?.length ?? "0"} s="SHA-256 sealed" />
      </section>
      
      <div className="two">
        <div className="panel">
          <span className="eyebrow">THREAT FIELD</span>
          <h3>Manipulation surface</h3>
          <div className="field">
            <div className="core">{risk}</div>
            {["URGENCY","SNEAKING","PRESSURE","COST","CONSENT"].map((x, i) => (
              <span className={`node node${i}`} key={x}>{x}</span>
            ))}
          </div>
        </div>
        <div className="panel">
          <span className="eyebrow">LIVE TELEMETRY</span>
          <h3>Investigation signals</h3>
          {["DOM structure ready","Visual hierarchy ready","Behavior probe ready","Evidence hashing ready","Risk engine ready"].map((x, i) => (
            <div className="event" key={x}>
              <span>●</span><time>0{i + 1}s</time>
              <p>{x}</p>
              <b>{i < 2 ? "READY" : "STAGED"}</b>
            </div>
          ))}
        </div>
      </div>
      
      <div className="section-title">
        <span className="eyebrow">LATEST INTELLIGENCE</span>
        <h3>Evidence-backed classifications</h3>
      </div>
      <FindingGrid />
    </>
  );
}

export default CommandCenter;
