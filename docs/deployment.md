# Deployment and reproducible local runbook

```bash
python -m venv .venv
# Windows activation: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -e ".[dev]"
python scripts/bootstrap.py
pytest -q
uvicorn demandpilot.api.main:app --reload
# Open a new terminal:
streamlit run dashboard/app.py
```

Open dashboard `http://localhost:8501`; Swagger docs `http://localhost:8000/docs`.

## Docker

```bash
docker compose up --build
```

The API generates synthetic data and trains at first startup. The dashboard talks to `http://api:8000`. Refresh dashboard after API startup if initially unavailable. `docker compose down -v` removes synthetic saved data. Requires Docker/Compose installed.

## curl examples

```bash
curl -X POST http://localhost:8000/forecast -H "Content-Type: application/json" -d '{"store_id":"HYD01","product_id":"P101","days":14}'
curl http://localhost:8000/inventory/alerts
curl -X POST http://localhost:8000/inventory/recommend -H "Content-Type: application/json" -d '{"forecast":[10,10,10,10,10,10,10,10,10,10,10,10],"on_hand":20,"lead_time_days":5,"review_period_days":7}'
```

Do not deploy to the public Internet as a production service without authentication, TLS, rate limiting, privacy safeguards and operations monitoring. SQLite is appropriate for a local educational demo, not concurrent enterprise scale.
