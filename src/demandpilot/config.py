"""Paths may be overridden with DEMANDPILOT_HOME."""
import os
from pathlib import Path
ROOT = Path(os.getenv("DEMANDPILOT_HOME", Path(__file__).resolve().parents[2]))
DATA = ROOT / "data" / "processed"
ARTIFACTS = ROOT / "artifacts"
REPORTS = ROOT / "reports"
SALES_FILE = DATA / "daily_sales.csv"
STOCK_FILE = DATA / "inventory.csv"
MODEL_FILE = ARTIFACTS / "forecast_model.txt"
META_FILE = ARTIFACTS / "metadata.json"
METRICS_FILE = ARTIFACTS / "metrics.json"
DB_FILE = DATA / "demandpilot.db"
