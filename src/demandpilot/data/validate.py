"""Validate canonical one-row-per-product-store-day sales."""
import pandas as pd
REQUIRED = {"date", "store_id", "product_id", "category", "price", "units_sold", "promo"}

def validate_sales(df: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED - set(df)
    if missing:
        raise ValueError(f"Sales columns missing: {sorted(missing)}")
    out = df.copy()
    out["date"] = pd.to_datetime(out["date"], errors="raise").dt.normalize()
    if out[list(REQUIRED)].isnull().any().any():
        raise ValueError("Required sales fields contain null values")
    for col in ("store_id", "product_id", "category"):
        out[col] = out[col].astype(str)
    for col in ("price", "units_sold", "promo"):
        out[col] = pd.to_numeric(out[col], errors="raise")
    if (out.units_sold < 0).any() or (out.price <= 0).any():
        raise ValueError("Units must be nonnegative and price must be positive")
    if (out.units_sold % 1 != 0).any() or (~out.promo.isin([0, 1])).any():
        raise ValueError("Units must be integers and promo must be 0/1")
    if out.duplicated(["date", "store_id", "product_id"]).any():
        raise ValueError("Duplicate product-store-day rows found")
    out = out.sort_values(["store_id", "product_id", "date"]).reset_index(drop=True)
    for _, group in out.groupby(["store_id", "product_id"], sort=False):
        if not (group.date.diff().dropna() == pd.Timedelta(days=1)).all():
            raise ValueError("Each product-store series must have consecutive days")
    return out

def validate_inventory(df: pd.DataFrame) -> pd.DataFrame:
    fields = {"store_id", "product_id", "on_hand", "on_order", "backorders", "lead_time_days", "unit_cost", "service_level"}
    if fields - set(df):
        raise ValueError(f"Inventory columns missing: {sorted(fields - set(df))}")
    out = df.copy()
    if out[list(fields)].isnull().any().any():
        raise ValueError("Inventory has missing fields")
    if out.duplicated(["store_id", "product_id"]).any():
        raise ValueError("Duplicate inventory records")
    if (out[["on_hand","on_order","backorders","lead_time_days","unit_cost"]] < 0).any().any():
        raise ValueError("Inventory quantities must be nonnegative")
    if (out.lead_time_days < 1).any() or (~out.service_level.between(0.5,0.999)).any():
        raise ValueError("Lead time or service level outside accepted range")
    return out
