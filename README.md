# Automated-Forensic-Detection — DARKTRACE Forensic OS v2.0

Unified rebuild of the Automated Forensic Detection and Risk Assessment of Dark Patterns in E-Commerce Interfaces.

## Integrated changes

- Automated-Forensic-Detection branding
- Animated welcome screen
- Live URL investigation workflow
- Browser acquisition with Playwright
- DOM and HTML forensic extraction
- XPath and element metadata
- Full-page screenshot evidence
- Screenshot evidence vault
- Multisignal dark-pattern correlation
- Behavioral/persistence probing when browser access is available
- Explainable Risk Analytics with concrete evidence examples
- SHA-256 evidence sealing
- Downloadable PDF forensic report
- Dark and high-contrast light themes
- Case management, Evidence Lab, Risk Analytics and Forensic Report views

## Backend

```bash
cd backend
python -m pip install -r requirements.txt
python -m playwright install chromium
python app.py
```

Backend: `http://localhost:5000`

## Frontend

```bash
cd frontend
npm install
npm start
```

Frontend: `http://localhost:3000`

## Notes

The application uses live browser evidence when the target URL can be rendered. If a target cannot be acquired, the interface clearly falls back to demo/inferred evidence instead of pretending that mock evidence is a real capture.
