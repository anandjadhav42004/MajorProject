# 🔎 Automated-Forensic-Detection

### Forensic Detection and Risk Assessment of Dark Patterns in E-Commerce Interfaces

> **An intelligent multimodal forensic analysis platform for detecting, investigating, scoring, and documenting deceptive user-interface patterns across e-commerce websites.**

---

## 🧠 Overview

**Automated-Forensic-Detection** is an advanced web-forensics and risk-assessment platform designed to automatically identify **dark patterns** used in e-commerce interfaces.

Dark patterns are user-interface techniques that intentionally influence, manipulate, confuse, or pressure users into making decisions they may not otherwise make.

Examples include:

* ⚠️ False urgency
* 🛒 Sneak into basket
* 💰 Hidden costs
* 🔄 Forced continuity
* 😳 Confirmshaming
* 🔐 Privacy manipulation

Instead of relying only on textual analysis, this system combines multiple forms of evidence:

```text
                    TARGET WEBSITE
                          │
                          ▼
              ┌─────────────────────┐
              │   Web Acquisition   │
              │      Engine         │
              └──────────┬──────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
       TEXT            DOM           VISUAL
     ANALYSIS        ANALYSIS       ANALYSIS
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                  BEHAVIORAL ANALYSIS
                         │
                         ▼
                MULTIMODAL CORRELATION
                         │
                         ▼
                 PATTERN CLASSIFICATION
                         │
                         ▼
                  RISK ASSESSMENT
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
       EVIDENCE LAB             RISK ANALYTICS
             │                       │
             └───────────┬───────────┘
                         ▼
                 FORENSIC REPORT
```

The goal is not simply to answer:

> **"Is this a dark pattern?"**

The system is designed to answer:

> **"What was detected, where was it detected, why was it classified as a dark pattern, what evidence supports the finding, how severe is the risk, and can the finding be reproduced?"**

---

# 🚀 Key Features

## 1. 🧠 Multimodal Dark Pattern Detection

The system analyzes multiple characteristics of a webpage rather than relying exclusively on text.

### Text

Detects suspicious phrases and language such as:

```text
"Only 2 left!"
"Hurry!"
"Offer expires soon"
"Accept all"
"No thanks, I don't want to save money"
```

### DOM

Analyzes:

* HTML elements
* Classes
* IDs
* Attributes
* Element hierarchy
* XPath
* Visibility
* Input states
* Buttons
* Checkboxes
* Radio buttons
* Forms

### Visual Signals

The system can inspect characteristics such as:

* Button prominence
* Font size
* Color emphasis
* Position
* Visual hierarchy
* Suspicious warning styling
* Pop-ups
* Overlays
* Page layout

### Behavioral Signals

Where supported, the forensic engine can investigate:

* Page reload persistence
* Dynamic countdown behavior
* Automatically selected options
* Interaction requirements
* Number of clicks
* State changes

---

# 📸 2. Evidence Lab

The **Evidence Lab** provides a forensic workspace for investigating detected patterns.

Each finding can contain:

```text
Evidence ID
      │
      ├── URL
      ├── Timestamp
      ├── Pattern Type
      ├── Confidence
      ├── Risk Level
      ├── Screenshot
      ├── Suspicious Element
      ├── Detected Text
      ├── DOM Information
      ├── XPath
      ├── HTML Snapshot
      └── Evidence Hash
```

The system is designed to preserve evidence rather than displaying only a numerical prediction.

### Example

```text
Evidence #DP-0042

Pattern:
FALSE URGENCY

Detected text:
"Only 2 left!"

Confidence:
94.2%

Risk:
HIGH

Element:
<div class="stock-warning">

XPath:
/html/body/main/div[2]/div[1]

Visibility:
true

Screenshot:
Captured automatically

Evidence Hash:
SHA-256
```

---

# 🔍 3. DOM-Level Forensic Analysis

The system records the underlying HTML responsible for a detection.

Example:

```json
{
  "pattern": "false_urgency",
  "element": "div",
  "text": "Only 2 left!",
  "class": "stock-warning",
  "xpath": "/html/body/main/div[2]/div[1]",
  "visibility": true
}
```

This makes the detection more explainable and reproducible.

Instead of:

```text
AI Prediction:
False Urgency
```

the platform can provide:

```text
Classification:
False Urgency

Reason:
Urgency language was detected within a visually prominent
element positioned near the purchase action.

Supporting Evidence:
• "Only 2 left!"
• High visual prominence
• Near purchase CTA
• Urgency styling
• Behavioral persistence
```

---

# ⚠️ 4. Advanced Risk Analytics

The platform calculates a multidimensional risk profile.

Example:

```text
OVERALL DARK PATTERN RISK
━━━━━━━━━━━━━━━━━━━━━━━━
82 / 100

Manipulation Severity       88
User Impact                 91
Financial Risk              74
Privacy Risk                62
Deception Probability       89
Persistence                 76
```

The dashboard does not merely display numbers.

Each category is accompanied by an explanation.

### False Urgency

```text
Detected:
"Only 2 left!"

Supporting signals:
• Urgency language
• Red visual emphasis
• Position near BUY NOW
• Countdown component

Assessment:
HIGH
```

### Sneak Into Basket

```text
Detected:
Protection plan checkbox

State:
Pre-selected

Potential impact:
Additional product/service may be added
without an explicit user action.
```

### Hidden Cost

```text
Detected:
Additional service fee

Observed behavior:
Fee appears after progressing toward checkout.

Potential impact:
User may initially perceive a lower price.
```

---

# 🧪 5. Six Dark Pattern Categories

## False Urgency

Creates artificial pressure by suggesting:

* Limited inventory
* Expiring deals
* Countdown timers
* High demand
* Other users competing for the item

---

## Sneak Into Basket

Attempts to add additional products or services without a clear intentional selection.

Examples:

* Pre-selected warranty
* Protection plan
* Donation
* Insurance
* Accessories

---

## Hidden Cost

Costs that are difficult to notice or are revealed later.

Examples:

* Service fees
* Processing fees
* Handling fees
* Mandatory charges
* Late shipping costs

---

## Forced Continuity

Subscription or trial interfaces designed to encourage continued payment or renewal.

Examples:

* Automatic renewal
* Free trial converting into paid subscription
* Difficult cancellation flow

---

## Confirmshaming

Uses guilt or embarrassment to discourage users from rejecting an offer.

Example:

```text
YES, SAVE MONEY

No thanks, I prefer paying more.
```

---

## Privacy Manipulation

Uses interface design to encourage broader data sharing or tracking.

Examples:

* Prominent "Accept All"
* Hidden rejection controls
* Pre-selected tracking
* Buried privacy settings

---

# 📊 6. Forensic Report Generation

The platform can generate a structured forensic report containing:

```text
Executive Summary

Website Information

Scan Metadata

Detected Dark Patterns

Risk Assessment

Detection Confidence

Supporting Evidence

Screenshots

DOM Evidence

Behavioral Findings

Evidence Hashes

Technical Findings

Recommendations
```

Reports are generated in a downloadable format for documentation and academic demonstration.

---

# 🖥️ 7. Modern Forensic Interface

The interface is designed as a modern forensic investigation dashboard.

### UI characteristics

* Dark forensic command-center theme
* Blue/black/white visual system
* Light mode
* Blue/green/white light theme
* Animated transitions
* Interactive dashboards
* Evidence cards
* Risk indicators
* Detection timelines
* Responsive layout
* Technical data visualization

---

# 🌗 8. Dark & Light Mode

## Dark Mode

The dark interface uses:

```text
Black
+
Deep Blue
+
White
```

This creates a forensic/security-console appearance.

## Light Mode

The light interface uses:

```text
White
+
Blue
+
Green
+
Black Text
```

with strong contrast for readability.

---

# ✨ 9. Animated Welcome Experience

The application begins with an animated forensic introduction screen.

The project title is displayed as:

> **WELCOME TO Automated-Forensic-Detection-and-Risk-Assessment-of-Dark-Patterns-in-E-Commerce-Interfaces**

The welcome experience then transitions into the main investigation dashboard.

---

# 🏗️ System Architecture

```text
┌─────────────────────────────────────────────┐
│                 FRONTEND                    │
│                                             │
│  Welcome Screen                             │
│  Dashboard                                  │
│  Scanner                                    │
│  Evidence Lab                               │
│  Risk Analytics                             │
│  Forensic Reports                           │
└──────────────────────┬──────────────────────┘
                       │
                       │ REST API
                       ▼
┌─────────────────────────────────────────────┐
│                  BACKEND                    │
│                                             │
│  Flask API                                  │
│       │                                     │
│       ├── Website Acquisition               │
│       ├── DOM Analyzer                      │
│       ├── Text Analyzer                     │
│       ├── Visual Analyzer                   │
│       ├── Behavioral Analyzer               │
│       ├── Pattern Classifier                │
│       ├── Risk Engine                       │
│       ├── Evidence Manager                  │
│       └── Report Generator                  │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Evidence Storage │
              │                  │
              │ Screenshots      │
              │ DOM Snapshots    │
              │ Metadata         │
              │ Hashes           │
              └──────────────────┘
```

---

# 🛠️ Technology Stack

## Frontend

* React
* JavaScript
* CSS
* Responsive UI
* Interactive dashboard components

## Backend

* Python
* Flask
* REST APIs

## Web Forensics

* Playwright
* Chromium
* DOM extraction
* Screenshot capture
* HTML inspection

## Analysis

* Python
* Regular-expression based pattern signals
* Multimodal evidence correlation
* Risk scoring
* Behavioral analysis

## Reporting

* ReportLab
* PDF generation

## Evidence Integrity

* SHA-256 hashing
* Timestamped evidence
* DOM snapshots
* Screenshot preservation

---

# 📁 Project Structure

```text
Automated-Forensic-Detection/
│
├── backend/
│   ├── app.py
│   ├── forensic_engine.py
│   ├── requirements.txt
│   │
│   └── evidence/
│
├── frontend/
│   ├── package.json
│   │
│   ├── public/
│   │   └── index.html
│   │
│   └── src/
│       ├── App.js
│       ├── App.css
│       ├── api.js
│       └── index.js
│
├── data/
│   └── evidence/
│
├── docs/
│   └── ARCHITECTURE.md
│
├── .gitignore
├── README.md
├── start_backend.bat
└── start_frontend.bat
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/sakshi-kadadekar/-Automated-Forensic-Detection-and-Risk-Assessment-of-Dark-Patterns-in-E-Commerce-Interfaces-.git
```

Enter the project:

```bash
cd -Automated-Forensic-Detection-and-Risk-Assessment-of-Dark-Patterns-in-E-Commerce-Interfaces-
```

---

# 🐍 Backend Setup

Navigate to the backend:

```bash
cd backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Chromium for Playwright:

```bash
python -m playwright install chromium
```

Start the backend:

```bash
python app.py
```

The backend API will normally be available at:

```text
http://localhost:5000
```

---

# ⚛️ Frontend Setup

Open another terminal.

Navigate to:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm start
```

The frontend will normally open at:

```text
http://localhost:3000
```

---

# 🔬 Example Investigation

Suppose the target website contains:

```text
ONLY 2 LEFT!

[ BUY NOW ]
```

The forensic engine can identify:

### Text Evidence

```text
"ONLY 2 LEFT!"
```

### DOM Evidence

```text
<div class="stock-warning">
    ONLY 2 LEFT!
</div>
```

### Visual Evidence

```text
High prominence
Warning-style presentation
Near purchase CTA
```

### Behavioral Evidence

```text
State persists after page reload
```

### Final Result

```text
Pattern:
FALSE URGENCY

Confidence:
94%

Risk:
HIGH

Reason:
Multiple independent signals support the
classification.
```

---

# 📈 Risk Scoring Model

The risk engine considers multiple dimensions rather than producing a single arbitrary label.

Conceptually:

```text
Risk Score =
    Manipulation Severity
    +
    User Impact
    +
    Financial Risk
    +
    Privacy Risk
    +
    Deception Probability
    +
    Persistence
```

The final score is normalized to:

```text
0 ─────────────────────── 100
LOW        MEDIUM        HIGH
```

Example:

```text
0–29    LOW
30–59   MEDIUM
60–79   HIGH
80–100  CRITICAL
```

---

# 🔐 Evidence Integrity

Each evidence package can be associated with a SHA-256 hash.

Example:

```text
Evidence Hash:

8d4e8b9c...
```

This allows investigators to determine whether stored evidence has been modified after acquisition.

---

# 🎯 Project Objectives

The project aims to:

1. Automate dark-pattern detection.
2. Combine textual and visual evidence.
3. Analyze webpage DOM structures.
4. Capture forensic screenshots.
5. Record suspicious UI elements.
6. Investigate behavioral signals.
7. Explain why a pattern was detected.
8. Calculate multidimensional risk.
9. Preserve evidence for investigation.
10. Generate downloadable forensic reports.
11. Provide an interactive investigation dashboard.
12. Demonstrate how AI-assisted web forensics can be applied to e-commerce interfaces.

---

# 🎓 Academic / Research Value

This project is particularly suitable for research and academic demonstration because it moves beyond simple keyword classification.

A conventional detector might produce:

```text
False Urgency
Confidence: 94%
```

Automated-Forensic-Detection attempts to provide:

```text
FALSE URGENCY

Confidence: 94%

Evidence:
✓ Urgency phrase detected
✓ Suspicious visual emphasis
✓ Element positioned near purchase CTA
✓ DOM evidence captured
✓ Screenshot captured
✓ Behavioral state recorded

Risk:
HIGH

Explanation:
Multiple independent signals indicate that
the interface may be attempting to create
artificial purchase pressure.
```

This makes the system more **interpretable, auditable, and forensic-oriented**.

---

# 🔮 Future Improvements

Potential future extensions include:

* Transformer-based multimodal models
* Vision-language models
* OCR-based screenshot analysis
* Computer vision layout detection
* Deep-learning dark-pattern classification
* Browser extension integration
* Automated multi-page crawling
* User-flow reconstruction
* Click-path analysis
* Network request analysis
* Cookie and tracker analysis
* Accessibility-based manipulation detection
* Evidence-chain visualization
* Database-backed case management
* PDF digital signatures
* Automated comparison between website versions
* Real-time dark-pattern monitoring

---

# ⚠️ Ethical Use

This project is intended for:

* Academic research
* Usability research
* Web-forensics experimentation
* Consumer-protection research
* Security research
* Interface auditing
* Educational demonstrations

Only analyze websites that you are authorized to test.

Do not use automated scanning to overload, disrupt, bypass security controls, or interfere with third-party systems.

---

# 👩‍💻 Project

**Automated-Forensic-Detection and Risk Assessment of Dark Patterns in E-Commerce Interfaces**

Developed as an academic/research project focused on:

> **Automated detection + forensic evidence + explainable risk assessment**

---

# ⭐ Why This Project Is Different

Traditional dark-pattern detection often focuses primarily on identifying suspicious language.

This project aims to combine:

```text
TEXT
 │
 ├──► DOM
 │
 ├──► VISUAL
 │
 ├──► BEHAVIOR
 │
 └──► INTERACTION
          │
          ▼
   MULTIMODAL EVIDENCE
          │
          ▼
    CLASSIFICATION
          │
          ▼
    RISK ASSESSMENT
          │
          ▼
   FORENSIC EVIDENCE
          │
          ▼
   INVESTIGATION REPORT
```

The result is a system designed not merely to **detect dark patterns**, but to **investigate and document them**.

---

## 📜 License

This project is intended primarily for academic and research purposes.

Add an appropriate open-source license if you intend to distribute the project publicly.
