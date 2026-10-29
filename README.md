# 📈 DemandPilot AI

**DemandPilot AI** demonstrates an integrated retail forecasting application built with Python, Pandas, LightGBM, scikit-learn, FastAPI, Streamlit, Plotly, SQLite and Docker Compose. It predicts daily observed sales and recommends reorder quantities using simulated inventory balances and supplier lead times.

[Setup](#local-installation--setup-guide) · [Architecture](#architecture--system-design-diagram) · [Detailed guide](PROJECT_GUIDE.md) · [Repository standard](docs/REPOSITORY_STANDARD.md)

## Visuals

![Measured model comparison on simulated data](<reports/figures/evaluation.svg>)

Existing project visual; diagrams and illustrative graphics are not evidence of a deployed application.

## Live Link / Demo

Run the local demo using the setup guide below. No public deployment URL has been verified for this documentation update.

## Key Features

| Section | Features |
|---|---|
| Overview | SKU-store totals, simulated risk alerts, recommended units, indicative order costs |
| Demand Forecast | Choose store/product, 7/14/30/60/90 days, daily plots, heuristic uncertainty ranges, CSV export |
| Inventory Planner | What-if lead times, stock, on-order, backorders, error uncertainty, service-level target |
| Model Evaluation | Seasonal baseline vs LightGBM; chronological validation and held-out test WAPE, MAE, RMSE |
| API | `GET /health`, `GET /catalog`, `POST /forecast`, `GET /inventory/alerts`, `POST /inventory/recommend`, `GET /metrics` |
| Engineering | Pytest, GitHub Actions CI, Docker Compose, Pydantic request validation, SQLite audit |

![Measured model comparison on simulated data](reports/figures/evaluation.svg)

## Tech Stack

![Python](https://img.shields.io/badge/Python-334155?style=flat-square) ![FastAPI](https://img.shields.io/badge/FastAPI-334155?style=flat-square) ![Streamlit](https://img.shields.io/badge/Streamlit-334155?style=flat-square) ![scikit-learn](https://img.shields.io/badge/scikit--learn-334155?style=flat-square) ![Pandas](https://img.shields.io/badge/Pandas-334155?style=flat-square) ![NumPy](https://img.shields.io/badge/NumPy-334155?style=flat-square) ![LightGBM](https://img.shields.io/badge/LightGBM-334155?style=flat-square) ![Docker](https://img.shields.io/badge/Docker-334155?style=flat-square)

Dependency versions and optional packages are defined in the repository manifests.

## Architecture / System Design Diagram

[Architecture documentation / diagram](<docs/architecture.md>)

## Local Installation & Setup Guide

Requires Python 3.10+ and an internet connection to install dependencies.

```bash
git clone https://github.com/harshakavali81-collab/DemandPilot-AI-Enterprise-AI-Demand-Forecasting-Inventory-Optimization-Platform.git
cd DemandPilot-AI-Enterprise-AI-Demand-Forecasting-Inventory-Optimization-Platform
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate
pip install -e ".[dev]"
python scripts/bootstrap.py
pytest -q
uvicorn demandpilot.api.main:app --reload
```

In **a second terminal** after activating your environment:

```bash
streamlit run dashboard/app.py
```

- **Dashboard:** http://localhost:8501
- **Swagger REST API:** http://localhost:8000/docs
- **Docker option:** `docker compose up --build`

`bootstrap.py` generates 420 days of daily sales for 8 products in 2 stores, writes SQLite tables, trains an actual LightGBM regression model, compares the baseline and exports model files and evaluation reports. No API key or paid cloud service is required.

## Challenges & Solutions

**Repository organization:** this project uses `src/`. Keeping those paths stable avoids breaking imports, asset links and deployment commands while the documentation follows a shared format. Project-specific technical limitations and prior release evidence are retained in [Project guide](PROJECT_GUIDE.md).

## Future Improvements

- Capture a reproducible end-to-end demo with runtime versions and sample inputs.
- Expand regression checks for invalid inputs and documented edge cases.
- Record measured results, data provenance and deployment limitations alongside each release.

## Scope and supporting evidence

### End-to-end Demand Forecasting & Inventory Optimization Platform — Portfolio Demo

[](https://github.com/harshakavali81-collab/DemandPilot-AI-Enterprise-AI-Demand-Forecasting-Inventory-Optimization-Platform/actions/workflows/ci.yml)

**DemandPilot AI** demonstrates an integrated retail forecasting application built with Python, Pandas, LightGBM, scikit-learn, FastAPI, Streamlit, Plotly, SQLite and Docker Compose. It predicts daily observed sales and recommends reorder quantities using simulated inventory balances and supplier lead times.

> **Important:** all bundled data is generated, not provided by real retailers. Forecast metrics, inventory balances and risk predictions are synthetic demonstration results. This is not a commercially validated inventory system and no live deployment has been verified.

## Repository Structure

| Location | Purpose |
| --- | --- |
| `src/` | Source modules |
| `tests/` | Tests |
| `docs/` | Documentation |
| `data/` | Data and samples |
| `scripts/` | Automation scripts |
| `.github/` | Issue forms, PR template and automated checks |

[Complete file inventory and workflow](docs/REPOSITORY_STANDARD.md). Runtime entry points retain their existing paths.

## Workflow & Tracking

Use the [bug and feature forms](https://github.com/harshakavali81-collab/DemandPilot-AI-Enterprise-AI-Demand-Forecasting-Inventory-Optimization-Platform/issues/new/choose) to define work with acceptance criteria. Keep tasks in Todo → In progress → Review → Done, and link a pull request with `Closes #<number>`. See [the maintenance workflow](docs/REPOSITORY_STANDARD.md#workflow).

## License

Original project software is available under the [MIT License](LICENSE). See [licensing scope](docs/LICENSING.md) for third-party and data exclusions.

