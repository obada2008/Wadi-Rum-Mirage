# Wadi Rum Mirage

**An explainable digital trust and cybersecurity learning experience inspired by Wadi Rum, Jordan.**

**Project owner & maintainer:** Obada Khader  
**Version:** 2.8.0  
**Languages:** Arabic (RTL) · English (LTR)  
**Stack:** Python · FastAPI · HTML · CSS · JavaScript

> A real fact is not proof that every requested action is legitimate.

Wadi Rum Mirage explores how messages can reference real institutions or credible details to encourage actions that have not been independently verified. It makes these patterns easier to examine through rule-based analysis, interactive visualizations, practical examples, and an experience inspired by Jordanian heritage.

## Features

| Module | Description |
|---|---|
| Message analysis | Highlights sensitive requests, urgency, and unsupported trust transfers. |
| Trust Graph 2.0 | Visualizes relationships and explains detected edges. |
| Passive URL Inspector | Examines URL structure and common warning signs without opening user-supplied links. |
| URL Anatomy Explorer | Breaks down protocol, subdomain, host, path, and query components. |
| Mirage Lab | Lets visitors test how changes in evidence and requests affect interpretation. |
| Threat Pattern Library | Offers bilingual synthetic scenarios and practical explanations. |
| Mirage Challenge | Ten educational rounds with a three-energy-cell game mechanic. |
| Wadi Rum Tour | Maps, credited heritage photography, and an illustrated interactive panorama. |
| Case Builder | Combines redacted message analysis, structural URL findings, and notes in an exportable JSON case. |
| Privacy Shield | Offers best-effort in-browser redaction before message submission. |
| Benchmark | Displays reproducible results from limited synthetic test cases. |

The interface supports Arabic and English, responsive navigation, and keyboard-accessible controls.

## Getting started

Requirements: Python 3.10+; pip.

### Windows

Run `start_windows.bat` from the extracted project folder. It installs the Python dependencies and launches the server at **http://127.0.0.1:8765**. Keep the terminal open while browsing.

### Manual setup

```bash
python -m pip install -r backend/requirements.txt
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8765
```

- Arabic: http://127.0.0.1:8765/?lang=ar
- English: http://127.0.0.1:8765/?lang=en
- API documentation: http://127.0.0.1:8765/docs

Live Demo: https://wadi-rum-mirage.onrender.com/
The analyzer and passive URL parsing run locally. Some map, image, and panorama resources rely on third-party connectivity.

## Project structure

```text
backend/        FastAPI app and analysis engine
frontend/       Bilingual UI, interaction scripts, styles, local assets
data/           Synthetic evaluation cases
scripts/        Reproducible evaluation tools
tests/          Regression and API tests
docs/           Research, limitations, security model, credits, evaluation results
start_windows.bat
```

## Tests and evaluation

Run tests from the repository root:

```bash
python -m pytest -q
python -m scripts.evaluate
```

Benchmark figures are from **120 synthetic, template-based examples**. They do not establish real-world scam detection accuracy or generalize to unseen threats. See `docs/research.md`, `docs/limitations.md`, and `docs/evaluation_results.json`.

## Safety and privacy

- **Not a real-time threat intelligence service.** User-supplied URLs are parsed, not visited or reputation-checked.
- **Not a trained AI model.** The released analysis engine uses transparent heuristic rules.
- **Not a certified forensic or anti-phishing tool.** Its findings are educational and may be wrong.
- Never submit passwords, live one-time codes, or private data. In-browser redaction is best-effort and cannot guarantee complete removal of personal information.
- The default server is for **local use**. Do not expose it to the internet without a separate security and privacy review.

## Why Wadi Rum?

Wadi Rum inspired the project's visual language and its central metaphor: a convincing appearance does not necessarily establish the underlying reality. Wadi Rum Protected Area is a UNESCO World Heritage Site, inscribed in 2011. [UNESCO reference](https://whc.unesco.org/en/list/1377).

## Credits and license

**Obada Khader** — project owner and maintainer.

The project is released under the **MIT License**. Third-party photography, mapping, and externally hosted resources retain their respective credits and licenses. See [CREDITS](docs/CREDITS.md) and the attribution links inside the website.
