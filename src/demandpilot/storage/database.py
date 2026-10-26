"""SQLite storage for simulated sales and prediction audit trail."""
import sqlite3
from datetime import datetime,timezone
from demandpilot.config import DB_FILE
def connection():
    DB_FILE.parent.mkdir(parents=True,exist_ok=True)
    return sqlite3.connect(DB_FILE)
def initialize(sales,inventory):
    with connection() as db:
        sales.to_sql("sales",db,if_exists="replace",index=False)
        inventory.to_sql("inventory",db,if_exists="replace",index=False)
        db.execute("""CREATE TABLE IF NOT EXISTS forecasts(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          created_at TEXT NOT NULL, store_id TEXT NOT NULL,
          product_id TEXT NOT NULL, days INTEGER NOT NULL,
          total_units REAL NOT NULL)""")
        db.execute("CREATE INDEX IF NOT EXISTS idx_forecasts_created ON forecasts(created_at)")
def record_forecast(store_id,product_id,days,total_units):
    with connection() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS forecasts(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          created_at TEXT NOT NULL, store_id TEXT NOT NULL,
          product_id TEXT NOT NULL, days INTEGER NOT NULL,
          total_units REAL NOT NULL)""")
        db.execute("INSERT INTO forecasts(created_at,store_id,product_id,days,total_units) VALUES(?,?,?,?,?)",
                   (datetime.now(timezone.utc).isoformat(),store_id,product_id,days,total_units))
