"""Synthetic, deterministic data: NOT real retail transactions."""
from datetime import date, timedelta
import argparse
import numpy as np
import pandas as pd
from demandpilot.config import DATA
from demandpilot.data.validate import validate_sales, validate_inventory

PRODUCTS = [
    ("P101","Wireless Mouse","Accessories",599,21),
    ("P102","Mechanical Keyboard","Accessories",2399,14),
    ("P103","USB-C Cable","Accessories",349,32),
    ("P104","Bluetooth Headphones","Audio",1999,12),
    ("P105","Portable Speaker","Audio",2999,10),
    ("P106","Smart Watch","Wearables",3499,9),
    ("P107","Laptop Stand","Office",1099,18),
    ("P108","Webcam","Office",1899,13),
]
STORES = ["HYD01","BLR01"]

def generate(days: int = 420, seed: int = 42, end: date = date(2026,9,30)):
    rng = np.random.default_rng(seed)
    start = end - timedelta(days=days-1)
    sales, inventory = [], []
    for si, store in enumerate(STORES):
        for pi, (sku, name, category, price, base) in enumerate(PRODUCTS):
            for t in range(days):
                day = start + timedelta(days=t)
                promo = int(rng.random() < 0.095)
                season = 1 + 0.16 * np.sin(2 * np.pi * t / 30 + pi)
                trend = 1 + t/days*0.13
                level = base*(1+si*0.16)*season*trend
                level *= (1.24 if day.weekday() >= 5 else 1.0)*(1.32 if promo else 1.0)
                units = int(rng.poisson(max(level,0.1)))
                sales.append([day,store,sku,category,round(price*(0.90 if promo else 1.0),2),units,promo])
            inventory.append([store,sku,name,int(rng.integers(12,180)),int(rng.integers(0,24)),0,int(rng.integers(3,9)),round(price*.62,2),.95])
    df = pd.DataFrame(sales, columns=["date","store_id","product_id","category","price","units_sold","promo"])
    stock = pd.DataFrame(inventory, columns=["store_id","product_id","product_name","on_hand","on_order","backorders","lead_time_days","unit_cost","service_level"])
    return validate_sales(df), validate_inventory(stock)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=420)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    if args.days < 100:
        ap.error("At least 100 days required")
    sales, stock = generate(args.days,args.seed)
    DATA.mkdir(parents=True,exist_ok=True)
    sales.to_csv(DATA/"daily_sales.csv",index=False)
    stock.to_csv(DATA/"inventory.csv",index=False)
    print(f"Generated {len(sales)} synthetic sales rows")
if __name__ == "__main__":
    main()
