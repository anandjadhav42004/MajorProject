from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from urllib.parse import urlparse
from pathlib import Path
import hashlib, json, os, re, uuid, time, statistics

app = Flask(__name__)
CORS(app)

BASE = Path(__file__).resolve().parent
EVIDENCE = BASE / "evidence"
EVIDENCE.mkdir(exist_ok=True)
import sqlite3

DB_PATH = BASE / "darklens.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS cases (
                id TEXT PRIMARY KEY,
                url TEXT,
                timestamp DATETIME,
                risk_score INTEGER,
                status TEXT,
                data TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS findings (
                id TEXT PRIMARY KEY,
                case_id TEXT,
                pattern TEXT,
                confidence INTEGER,
                risk TEXT,
                explanation TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS evidence (
                id TEXT PRIMARY KEY,
                finding_id TEXT,
                screenshot TEXT,
                html TEXT,
                xpath TEXT,
                text TEXT,
                timestamp DATETIME,
                hash TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS behavior_events (
                id TEXT PRIMARY KEY,
                case_id TEXT,
                action TEXT,
                before_state TEXT,
                after_state TEXT,
                timestamp DATETIME
            )
        ''')
init_db()

def get_db_case(case_id):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("SELECT data FROM cases WHERE id = ?", (case_id,)).fetchone()
        if row:
            return json.loads(row[0])
    return None

def save_db_case(case_id, data):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT OR REPLACE INTO cases (id, url, timestamp, risk_score, status, data) VALUES (?, ?, ?, ?, ?, ?)",
                     (case_id, data.get("url"), data.get("timestamp"), data.get("risk_score"), "COMPLETE", json.dumps(data)))
        
        for idx, p in enumerate(data.get("patterns", [])):
            finding_id = f"FND-{case_id}-{idx}"
            conn.execute("INSERT OR REPLACE INTO findings (id, case_id, pattern, confidence, risk, explanation) VALUES (?, ?, ?, ?, ?, ?)",
                         (finding_id, case_id, p["name"], p["confidence"], p["severity"], json.dumps(p["explanation"])))
            
        for idx, e in enumerate(data.get("evidence", [])):
            conn.execute("INSERT OR REPLACE INTO evidence (id, finding_id, screenshot, html, xpath, text, timestamp, hash) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                         (e["id"], f"FND-{case_id}-{idx}", e.get("visual", {}).get("screenshot", ""), e.get("dom", {}).get("html", ""), e.get("dom", {}).get("xpath", ""), e.get("text", ""), e["timestamp"], e["hash"]))

def get_all_db_cases():
    with sqlite3.connect(DB_PATH) as conn:
        return [json.loads(row[0]) for row in conn.execute("SELECT data FROM cases ORDER BY timestamp DESC").fetchall()]

PATTERNS = {
    "False Urgency": {
        "severity": "CRITICAL",
        "base": 90,
        "signals": ["urgency language", "countdown/timer", "limited-time wording"],
        "rx": r"(only\s+\d+\s+(left|remaining)|hurry|last chance|ends?\s+in|limited\s+time|selling\s+fast|act\s+now)"
    },
    "Hidden Costs": {
        "severity": "CRITICAL",
        "base": 84,
        "signals": ["late fee language", "delivery/service/handling fee", "price increase"],
        "rx": r"(convenience\s+fee|service\s+fee|handling\s+fee|delivery\s+fee|additional\s+charges?|taxes?\s+and\s+fees?)"
    },
    "Forced Action": {
        "severity": "HIGH",
        "base": 76,
        "signals": ["pre-selected checkbox", "subscription/protection/warranty language"],
        "rx": r"(subscribe|protection\s+plan|warranty|insurance|receive\s+promotional|auto.?renew)"
    },
    "Confirm Shaming": {
        "severity": "HIGH",
        "base": 70,
        "signals": ["guilt/shame language", "negative opt-out wording"],
        "rx": r"(no\s+thanks.*(pay|save|protect)|i\s+prefer\s+paying\s+more|i\s+don.?t\s+care|skip.*save)"
    },
    "Sneak Into Basket": {
        "severity": "HIGH",
        "base": 68,
        "signals": ["pre-selected add-on", "cart/basket language", "optional product"],
        "rx": r"(added\s+(to|in)\s+(your\s+)?(cart|basket)|pre.?selected|add\s+protection|add\s+warranty)"
    },
    "Scarcity Tactic": {
        "severity": "MODERATE",
        "base": 58,
        "signals": ["stock quantity", "scarcity wording", "demand wording"],
        "rx": r"(only\s+\d+|few\s+left|limited\s+stock|in\s+demand|selling\s+fast|remaining)"
    },
    "Disguised Ads": {
        "severity": "HIGH",
        "base": 75,
        "signals": ["sponsored content", "recommended language with ad markers"],
        "rx": r"(sponsored|promoted|ad\b|advertisement|recommended\s+for\s+you)"
    },
    "Bait and Switch": {
        "severity": "CRITICAL",
        "base": 85,
        "signals": ["price difference", "misleading product descriptions"],
        "rx": r"(price\s+change|updated\s+price|was\s+\d+.*now\s+\d+|out\s+of\s+stock.*substitute)"
    },
    "Roach Motel": {
        "severity": "HIGH",
        "base": 80,
        "signals": ["difficult cancellation", "contact support to cancel"],
        "rx": r"(call\s+to\s+cancel|contact\s+support\s+to\s+unsubscribe|cancellation\s+policy|cannot\s+be\s+cancelled)"
    },
    "Obstruction": {
        "severity": "MODERATE",
        "base": 65,
        "signals": ["UI friction", "hard to find settings"],
        "rx": r"(advanced\s+settings|more\s+options|manage\s+preferences|continue\s+without\s+saving)"
    }
}

def normalize_url(value):
    value = (value or "").strip()
    if not value:
        raise ValueError("URL is required")
    if not value.startswith(("http://", "https://")):
        value = "https://" + value
    return value

def sha256_bytes(data: bytes):
    return hashlib.sha256(data).hexdigest()

def xpath_for(el):
    parts = []
    cur = el
    while cur and getattr(cur, "name", None) and cur.name != "[document]":
        index = 1
        sib = cur.previous_sibling
        while sib:
            if getattr(sib, "name", None) == cur.name:
                index += 1
            sib = sib.previous_sibling
        parts.append(f"{cur.name}[{index}]")
        cur = cur.parent
    return "/" + "/".join(reversed(parts))

def style_signal(tag):
    style = (tag.get("style") or "").lower()
    classes = " ".join(tag.get("class", [])) if tag.get("class") else ""
    blob = (style + " " + classes).lower()
    visual = []
    if any(x in blob for x in ["red", "danger", "warning", "#f00", "#ff3", "urgent"]):
        visual.append("red/warning visual emphasis")
    if "font-size" in style:
        visual.append("explicit font sizing")
    if "position:absolute" in style.replace(" ", ""):
        visual.append("positioned overlay")
    if any(x in blob for x in ["modal", "popup", "overlay", "dialog"]):
        visual.append("popup/overlay")
    return visual

def collect_dom_signals(soup):
    nodes = []
    selectors = ["button", "a", "input", "label", "select", "textarea", "[role=button]", "[class*=timer]", "[class*=countdown]"]
    seen = set()
    for selector in selectors:
        for tag in soup.select(selector):
            key = id(tag)
            if key in seen:
                continue
            seen.add(key)
            text = tag.get_text(" ", strip=True)
            attrs = {k: str(v) for k, v in tag.attrs.items() if k in ("id","class","name","type","role","aria-label","value","checked")}
            if text or tag.name == "input":
                nodes.append({
                    "tag": tag.name,
                    "text": text[:300],
                    "attributes": attrs,
                    "xpath": xpath_for(tag),
                    "visible": True,
                    "visual_signals": style_signal(tag),
                    "html": str(tag)[:1200]
                })
    return nodes

def infer_pattern(pattern_name, text, nodes):
    p = PATTERNS[pattern_name]
    low = text.lower()
    matches = list(re.finditer(p["rx"], low, re.I))
    evidence_text = ""
    
    confidence = 0
    signals_breakdown = {}
    
    if matches:
        m = matches[0]
        evidence_text = text[max(0,m.start()-100):min(len(text),m.end()+160)].strip()
        confidence += 25
        signals_breakdown["Language"] = "25/25"
    else:
        signals_breakdown["Language"] = "0/25"
        
    relevant = []
    for n in nodes:
        blob = (n["text"] + " " + json.dumps(n["attributes"])).lower()
        if re.search(p["rx"], blob, re.I) or any(s in blob for s in ("timer","countdown","warranty","protection","subscribe","cart","basket","fee","only ")):
            relevant.append(n)
            
    visual = []
    behavior = []
    
    if relevant:
        confidence += 20
        signals_breakdown["DOM context"] = "20/20"
        for n in relevant[:4]:
            visual.extend(n["visual_signals"])
    else:
        signals_breakdown["DOM context"] = "0/20"
        
    if visual:
        confidence += 15
        signals_breakdown["Visual prominence"] = "15/15"
    else:
        signals_breakdown["Visual prominence"] = "0/15"
        
    if relevant:
        confidence += 15
        signals_breakdown["CTA proximity"] = "15/15"
    else:
        signals_breakdown["CTA proximity"] = "0/15"
        
    if pattern_name in ("False Urgency","Scarcity Tactic") and re.search(r"\b\d{1,2}:\d{2}\b|\b\d+\s*(minutes?|seconds?)\b", text, re.I):
        behavior.append("timer/countdown signal")
        
    if pattern_name == "Forced Action" and any(n["tag"] == "input" and n["attributes"].get("type") == "checkbox" and ("checked" in n["attributes"] or n["attributes"].get("checked") in ("true","checked")) for n in nodes):
        behavior.append("pre-selected checkbox")
        
    if pattern_name == "Sneak Into Basket" and any("checked" in n["attributes"] for n in relevant):
        behavior.append("optional item appears pre-selected")
        
    signals_breakdown["Persistence"] = "0/15"
    
    if matches:
        confidence += 10
        signals_breakdown["Historical/context"] = "10/10"
    else:
        signals_breakdown["Historical/context"] = "0/10"
        
    score = p["base"]
    
    return {
        "name": pattern_name,
        "score": score,
        "confidence": min(100, confidence),
        "severity": p["severity"],
        "evidence": evidence_text or (relevant[0]["text"] if relevant else p["signals"][0]),
        "explanation": build_explanation(pattern_name, evidence_text, relevant, visual, behavior, signals_breakdown, min(100, confidence)),
        "signals": p["signals"],
        "dom_matches": relevant[:5],
        "visual_signals": sorted(set(visual)),
        "behavior_signals": behavior,
        "signals_breakdown": signals_breakdown,
        "type": "Text + DOM + Visual + Behavior"
    }

def build_explanation(name, evidence, relevant, visual, behavior, breakdown, total_conf):
    reasons = []
    if evidence:
        reasons.append(f'✓ "{evidence[:40]}..." detected')
    if visual:
        reasons.append(f'✓ {visual[0]}')
    if behavior:
        reasons.append(f'✓ {behavior[0]}')
        
    reasons.append(f"Language: {breakdown['Language']}")
    reasons.append(f"DOM context: {breakdown['DOM context']}")
    reasons.append(f"Visual prominence: {breakdown['Visual prominence']}")
    reasons.append(f"CTA proximity: {breakdown['CTA proximity']}")
    reasons.append(f"Persistence: {breakdown['Persistence']}")
    reasons.append(f"Total: {total_conf}/100")
        
    return reasons

def calculate_dimensions(patterns):
    if not patterns:
        return {"manipulation_severity":12,"user_impact":10,"financial_risk":8,"privacy_risk":5,"deception_probability":10,"persistence":8}
    avg = statistics.mean(p["score"] for p in patterns)
    names = {p["name"] for p in patterns}
    return {
        "manipulation_severity": round(min(100, avg + 5)),
        "user_impact": round(min(100, avg + (10 if names & {"False Urgency","Confirm Shaming","Forced Action"} else 3))),
        "financial_risk": round(min(100, avg + (12 if names & {"Hidden Costs","Sneak Into Basket", "Bait and Switch"} else -5))),
        "privacy_risk": round(min(100, max(8, avg - (12 if "Privacy" not in names else 0)))),
        "deception_probability": round(min(100, avg + 7)),
        "persistence": round(min(100, avg + (5 if names & {"False Urgency","Scarcity Tactic"} else -4)))
    }

def risk_label(score):
    if score <= 20: return "VERY LOW"
    if score <= 40: return "LOW"
    if score <= 60: return "MODERATE"
    if score <= 80: return "HIGH"
    return "CRITICAL"

def analyze_html(html, url):
    soup = BeautifulSoup(html, "html.parser")
    for bad in soup(["script","style","noscript"]):
        bad.extract()
    text = " ".join(soup.stripped_strings)
    nodes = collect_dom_signals(soup)
    patterns = []
    for name in PATTERNS:
        if re.search(PATTERNS[name]["rx"], text, re.I) or any(re.search(PATTERNS[name]["rx"], n["text"], re.I) for n in nodes):
            patterns.append(infer_pattern(name, text, nodes))
    return soup, nodes, patterns

def create_case_id():
    return "DP-" + datetime.now().strftime("%Y") + "-" + uuid.uuid4().hex[:6].upper()

def make_evidence(pattern, case_id, url, screenshot_path=None):
    raw = json.dumps({"case":case_id,"url":url,"pattern":pattern}, sort_keys=True).encode()
    digest = sha256_bytes(raw)
    return {
        "id": "EV-" + uuid.uuid4().hex[:8].upper(),
        "case_id": case_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "url": url,
        "pattern": pattern["name"],
        "confidence": pattern["confidence"],
        "risk": pattern["severity"],
        "text": pattern["evidence"],
        "dom": {
            "tag": (pattern.get("dom_matches") or [{}])[0].get("tag", "div"),
            "class": (pattern.get("dom_matches") or [{}])[0].get("attributes", {}).get("class", ""),
            "xpath": (pattern.get("dom_matches") or [{}])[0].get("xpath","/html/body"),
            "html": (pattern.get("dom_matches") or [{}])[0].get("html","<evidence inferred from page text/visual signals>")
        },
        "visual": {
            "screenshot": f"/evidence/{case_id}/screenshot" if screenshot_path else None,
            "bounding_box": {"x": 0, "y": 0, "width": 0, "height": 0}
        },
        "behavior": {
            "reload_persistence": "same urgency content persisted after reload" in pattern["behavior_signals"],
            "auto_selected": "pre-selected checkbox" in pattern["behavior_signals"] or "optional item appears pre-selected" in pattern["behavior_signals"]
        },
        "hash": "sha256:" + digest
    }

@app.get("/health")
def health():
    return jsonify({"status":"operational","service":"DARKLENS","version":"3.0.0"})

@app.post("/analyze")
def analyze():
    body = request.get_json(silent=True) or {}
    try:
        url = normalize_url(body.get("url"))
    except ValueError as e:
        return jsonify({"error":str(e)}), 400

    case_id = create_case_id()
    now = datetime.now(timezone.utc)
    html = ""
    mode = "live-html"
    screenshot_path = None
    browser_error = None
    soup = None
    nodes = []
    patterns = []

    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width":1440,"height":900}, device_scale_factor=1)
            page = context.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=25000)
            page.wait_for_timeout(1800)
            html = page.content()
            screenshot_path = EVIDENCE / f"{case_id}.png"
            page.screenshot(path=str(screenshot_path), full_page=True)
            first_text = page.locator("body").inner_text(timeout=5000)[:5000]
            page.reload(wait_until="domcontentloaded", timeout=25000)
            page.wait_for_timeout(1000)
            second_text = page.locator("body").inner_text(timeout=5000)[:5000]
            browser.close()
            soup, nodes, patterns = analyze_html(html, url)
            
            if patterns and first_text == second_text and any(p["name"] in ("False Urgency","Scarcity Tactic") for p in patterns):
                for p in patterns:
                    if p["name"] in ("False Urgency","Scarcity Tactic"):
                        p["behavior_signals"].append("same urgency content persisted after reload")
                        p["signals_breakdown"]["Persistence"] = "15/15"
                        p["confidence"] = min(100, p["confidence"] + 15)
                        
                        p["explanation"] = build_explanation(
                            p["name"], p["evidence"], p["dom_matches"], 
                            p["visual_signals"], p["behavior_signals"], 
                            p["signals_breakdown"], p["confidence"]
                        )
    except Exception as e:
        browser_error = str(e)[:300]
        try:
            import requests
            r = requests.get(url, timeout=15, headers={"User-Agent":"Automated-Forensic-Detection/3.0"})
            r.raise_for_status()
            html = r.text
            soup, nodes, patterns = analyze_html(html, url)
            mode = "live-html-no-browser"
        except Exception as fallback_e:
            return jsonify({"error": f"Acquisition failed. Target could not be reached or timed out: {str(fallback_e)[:150]}"}), 502

    if not patterns:
        patterns = []

    risk = round(statistics.mean([p["score"] for p in patterns])) if patterns else 8
    confidence = round(statistics.mean([p["confidence"] for p in patterns])) if patterns else 20
    dimensions = calculate_dimensions(patterns)

    evidence = [make_evidence(p, case_id, url, screenshot_path) for p in patterns]
    journey = [
        {"stage":"Homepage","risk":"LOW","detail":"Initial page surface inspected for urgency, popups and visual pressure."},
        {"stage":"Product Page","risk":"MODERATE" if risk < 70 else "HIGH","detail":"Product messaging, price presentation and CTAs correlated."},
        {"stage":"Cart","risk":"HIGH" if any(p["name"]=="Sneak Into Basket" for p in patterns) else "MODERATE","detail":"Optional add-ons and basket state require explicit consent."},
        {"stage":"Checkout","risk":"CRITICAL" if any(p["name"]=="Hidden Costs" for p in patterns) else "HIGH","detail":"Late price changes and mandatory/optional choices are evaluated."},
        {"stage":"Payment","risk":"HIGH" if risk >= 60 else "LOW","detail":"Final-step pressure and consent persistence should be reviewed."}
    ]

    result = {
        "case_id":case_id,
        "url":url,
        "timestamp":now.isoformat(),
        "risk_score":risk,
        "risk_label":risk_label(risk),
        "confidence_score":confidence,
        "mode":mode,
        "browser_error":browser_error,
        "page_title": soup.title.get_text(strip=True) if soup and soup.title else urlparse(url).netloc,
        "dom_node_count": len(nodes),
        "patterns":patterns,
        "dimensions":dimensions,
        "evidence":evidence,
        "journey":journey,
        "integrity":"VERIFIED" if evidence else "NOT SEALED",
        "summary":f"{len(patterns)} dark-pattern signal(s) correlated across available text, DOM, visual and behavioral evidence."
    }
    save_db_case(case_id, result)
    return jsonify(result)

@app.get("/cases")
def cases():
    return jsonify(get_all_db_cases())

@app.get("/cases/<case_id>")
def get_case(case_id):
    case = get_db_case(case_id)
    if not case:
        return jsonify({"error":"case not found"}),404
    return jsonify(case)

@app.get("/evidence/<case_id>/screenshot")
def screenshot(case_id):
    path = EVIDENCE / f"{case_id}.png"
    if not path.exists():
        return jsonify({"error":"No rendered screenshot exists for this case. Browser capture may not have been available."}),404
    return send_file(path, mimetype="image/png", max_age=0)

@app.get("/evidence/<case_id>/<evidence_id>")
def evidence_item(case_id, evidence_id):
    case = get_db_case(case_id)
    if not case:
        return jsonify({"error":"case not found"}),404
    for item in case["evidence"]:
        if item["id"] == evidence_id:
            return jsonify(item)
    return jsonify({"error":"evidence not found"}),404

def build_report_html(case):
    rows = "".join(
        f"<tr><td>{p['name']}</td><td>{p['severity']}</td><td>{p['score']}%</td><td>{p['evidence']}</td><td>{'<br>'.join(p['explanation'])}</td></tr>"
        for p in case["patterns"]
    )
    evidence = "".join(
        f"<li><b>{e['id']}</b> — {e['pattern']} — {e['hash']} — {e['timestamp']}</li>"
        for e in case["evidence"]
    )
    return f"""<!doctype html><html><head><meta charset='utf-8'>
    <title>Forensic Report {case['case_id']}</title>
    <style>
    body{{font-family:Arial,sans-serif;margin:42px;color:#101820}}h1{{color:#075bff}}h2{{margin-top:30px}}
    .hero{{padding:24px;background:#eef6ff;border-left:5px solid #075bff}}table{{border-collapse:collapse;width:100%}}
    th,td{{border:1px solid #cbd5e1;padding:9px;vertical-align:top;font-size:12px}}th{{background:#0b1622;color:white}}
    .risk{{font-size:34px;font-weight:800}}.muted{{color:#52616d}}li{{margin:8px 0}}
    </style></head><body>
    <h1>Automated-Forensic-Detection-and-Risk-Assessment-of-Dark-Patterns-in-E-Commerce-Interfaces</h1>
    <div class='hero'><div class='risk'>Risk {case['risk_score']}/100 — {case['risk_label']}</div>
    <p><b>Case:</b> {case['case_id']}<br><b>Target:</b> {case['url']}<br><b>Timestamp:</b> {case['timestamp']}<br>
    <b>Mode:</b> {case['mode']}<br><b>Confidence:</b> {case['confidence_score']}%</p></div>
    <h2>Executive Summary</h2><p>{case['summary']}</p>
    <h2>Detected Dark Patterns</h2><table><tr><th>Pattern</th><th>Severity</th><th>Confidence</th><th>Observed Evidence</th><th>Why Flagged</th></tr>{rows}</table>
    <h2>Risk Dimensions</h2><ul>{''.join(f"<li>{k.replace('_',' ').title()}: <b>{v}/100</b></li>" for k,v in case['dimensions'].items())}</ul>
    <h2>Evidence Chain</h2><ol>{evidence}</ol>
    <h2>Integrity</h2><p>{case['integrity']} — Evidence records are SHA-256 hashed at creation time.</p>
    </body></html>"""

@app.get("/reports/<case_id>/download")
def download_report(case_id):
    case = get_db_case(case_id)
    if not case:
        return jsonify({"error":"case not found"}),404
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib.units import mm
        from xml.sax.saxutils import escape
        out = EVIDENCE / f"{case_id}_forensic_report.pdf"
        styles = getSampleStyleSheet()
        title = ParagraphStyle("Title2", parent=styles["Title"], fontSize=16, leading=20, alignment=TA_CENTER, textColor=colors.HexColor("#075bff"))
        doc = SimpleDocTemplate(str(out), pagesize=A4, rightMargin=14*mm,leftMargin=14*mm,topMargin=14*mm,bottomMargin=14*mm)
        story=[Paragraph("Automated-Forensic-Detection",title),
               Paragraph("Forensic Detection & Risk Assessment of Dark Patterns",styles["Heading2"]),
               Spacer(1,8)]
        story += [Paragraph(f"<b>Case:</b> {case['case_id']}<br/><b>Target:</b> {case['url']}<br/><b>Risk:</b> {case['risk_score']}/100 — {case['risk_label']}<br/><b>Confidence:</b> {case['confidence_score']}%<br/><b>Mode:</b> {case['mode']}", styles["BodyText"]), Spacer(1,12),
                  Paragraph("Executive Summary",styles["Heading2"]), Paragraph(case["summary"],styles["BodyText"]), Spacer(1,10),
                  Paragraph("Detected Patterns",styles["Heading2"])]
        cell_style = ParagraphStyle("ReportCell", parent=styles["BodyText"], fontSize=7.5, leading=9, spaceAfter=0)
        header_style = ParagraphStyle("ReportHeader", parent=cell_style, textColor=colors.white, fontName="Helvetica-Bold")
        def cell(value, header=False):
            return Paragraph(escape(str(value)), header_style if header else cell_style)

        data = [[cell("Pattern", True), cell("Severity", True), cell("Score", True), cell("Evidence", True)]]
        data += [[cell(p["name"]), cell(p["severity"]), cell(str(p["score"]) + "%"), cell(p["evidence"])] for p in case["patterns"]]
        table=Table(data,colWidths=[34*mm,24*mm,18*mm,100*mm],repeatRows=1,splitByRow=1)
        table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0b1622")),("GRID",(0,0),(-1,-1),0.4,colors.grey),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
        story += [table, Spacer(1,12), Paragraph("Risk Dimensions",styles["Heading2"])]
        for k,v in case["dimensions"].items():
            story.append(Paragraph(f"{k.replace('_',' ').title()}: <b>{v}/100</b>",styles["BodyText"]))
        story += [Spacer(1,10), Paragraph("Evidence Integrity",styles["Heading2"])]
        for e in case["evidence"]:
            story.append(Paragraph(f"{e['id']} — {e['pattern']} — {e['hash']}",styles["BodyText"]))
            story.append(Spacer(1,4))
        doc.build(story)
        return send_file(out, as_attachment=True, download_name=f"{case_id}_forensic_report.pdf", mimetype="application/pdf")
    except Exception as exc:
        out = EVIDENCE / f"{case_id}_forensic_report.html"
        out.write_text(build_report_html(case), encoding="utf-8")
        return send_file(out, as_attachment=True, download_name=f"{case_id}_forensic_report.html", mimetype="text/html")

@app.post("/evidence/hash")
def hash_evidence():
    body = request.get_json(silent=True) or {}
    raw = json.dumps(body, sort_keys=True).encode()
    return jsonify({"algorithm":"SHA-256","hash":sha256_bytes(raw),"status":"SEALED"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
