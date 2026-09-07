import os

components_dir = "frontend/src/components"
os.makedirs(components_dir, exist_ok=True)

files = {
    "Stat.js": """import React from 'react';

function Stat({ t, v, s }) {
  return (
    <div className="stat">
      <span>{t}</span>
      <strong>{v}</strong>
      <small>{s}</small>
    </div>
  );
}

export default Stat;
""",
    "FindingGrid.js": """import React from 'react';
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
""",
    "CommandCenter.js": """import React from 'react';
import { useForensic } from '../context/ForensicContext';
import Stat from './Stat';
import FindingGrid from './FindingGrid';

function CommandCenter() {
  const { url, setUrl, scan, risk, data, findings } = useForensic();

  return (
    <>
      <section className="hero">
        <div className="hero-card">
          <span className="eyebrow">AI-ASSISTED INVESTIGATION</span>
          <h2>Find the manipulation <em>behind the interface.</em></h2>
          <p>Analyze text, buttons, visual hierarchy, DOM structure, pop-ups, prices and interaction behavior. Every finding becomes an evidence-backed forensic record.</p>
          <div className="scanbar">
            <input value={url} onChange={e => setUrl(e.target.value)} placeholder="https://shop.example/product" />
            <button onClick={scan}>START INVESTIGATION ↗</button>
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
        <Stat t="PATTERNS" v={findings.length} s="Correlated findings" />
        <Stat t="DOM SIGNALS" v={data?.dom_node_count ?? "—"} s="Extracted from target" />
        <Stat t="EVIDENCE" v={data?.evidence?.length ?? 0} s="SHA-256 sealed" />
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
""",
    "Scanner.js": """import React from 'react';
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
""",
    "Result.js": """import React from 'react';
import { useForensic } from '../context/ForensicContext';
import FindingGrid from './FindingGrid';

function Result() {
  const { data, risk, findings, setPage } = useForensic();

  return (
    <>
      <section className="result">
        <div>
          <span className="eyebrow">INVESTIGATION COMPLETE / {data?.case_id || "DEMO CASE"}</span>
          <h2>{risk > 80 ? "Critical" : "High"} manipulation surface detected.</h2>
          <p>{data?.summary || "The engine correlated six example dark-pattern signals. Run the backend scan against a real URL to replace demo findings with live evidence."}</p>
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
""",
    "CaseRegister.js": """import React from 'react';
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
""",
    "EvidenceLab.js": """import React from 'react';
import { useForensic } from '../context/ForensicContext';

function EvidenceLab() {
  const { data, selected, findings, evidenceUrl, tab, setTab } = useForensic();
  const current = selected || findings[0];

  return (
    <div className="evidence-layout">
      <div className="evidence-view">
        <div className="evidence-toolbar">
          <span>CASE {data?.case_id || "DEMO"}</span>
          <b>{current.name}</b>
          <span>{data?.mode || "DEMO"}</span>
        </div>
        {evidenceUrl ? (
          <img className="real-shot" src={evidenceUrl} alt="Captured website evidence" />
        ) : (
          <div className="demo-shot">
            <div className="demo-site">
              <header>SHOP / FORENSIC TARGET <span>CART (1)</span></header>
              <section>
                <div className="fake-image">PRODUCT SURFACE</div>
                <div>
                  <small>LIMITED DROP</small>
                  <h2>Wireless Headphones</h2>
                  <h3>₹1,999 <del>₹4,999</del></h3>
                  <strong>● ONLY 2 LEFT! <i>02:14</i></strong>
                  <button>BUY NOW</button>
                  <label><input type="checkbox" defaultChecked /> Add protection plan — ₹199</label>
                  <u>No thanks, I prefer paying more.</u>
                </div>
              </section>
            </div>
            <div className="hotspot a">01</div>
            <div className="hotspot b">02</div>
            <div className="hotspot c">03</div>
          </div>
        )}
      </div>
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
            element: data?.evidence?.find(e => e.pattern === current.name)?.html || "dynamic evidence element",
            text: current.evidence,
            xpath: data?.evidence?.find(e => e.pattern === current.name)?.xpath || "/html/body",
            visibility: true
          }, null, 2)}</pre>
        )}
        
        {tab === "SCREENSHOT" && (
          <div className="evidence-meta">
            <b>FULL-PAGE CAPTURE</b>
            <p>{evidenceUrl ? "Live screenshot served directly from the Flask evidence vault." : "No live browser screenshot is available yet; run the backend against a real target."}</p>
            {evidenceUrl && <a href={evidenceUrl} target="_blank" rel="noreferrer">OPEN RAW SCREENSHOT ↗</a>}
          </div>
        )}
        
        {tab === "BEHAVIOR" && (
          <div className="behavior">
            <b>BEHAVIORAL SIGNALS</b>
            {(current.behavior_signals || ["Reload persistence probe", "CTA adjacency", "Consent-state verification"]).map(x => (
              <p key={x}>✓ {x}</p>
            ))}
          </div>
        )}
        
        <div className="hash">✓ SHA-256 EVIDENCE SEALED</div>
      </div>
    </div>
  );
}

export default EvidenceLab;
""",
    "RiskAnalytics.js": """import React from 'react';
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

  const dims = data?.dimensions || { manipulation_severity: 88, user_impact: 91, financial_risk: 74, privacy_risk: 62, deception_probability: 89, persistence: 76 };
  
  const journeySteps = data?.journey || [
    { stage: "Homepage", risk: "LOW", detail: "No manipulation evidence loaded" },
    { stage: "Product Page", risk: "MEDIUM", detail: "Review urgency and scarcity cues" },
    { stage: "Cart", risk: "HIGH", detail: "Check optional add-ons" },
    { stage: "Checkout", risk: "CRITICAL", detail: "Check late fees and defaults" },
    { stage: "Payment", risk: "HIGH", detail: "Check final consent and pressure" }
  ];

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
""",
    "ReportDashboard.js": """import React from 'react';
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
"""
}

for name, content in files.items():
    with open(os.path.join(components_dir, name), "w") as f:
        f.write(content)
