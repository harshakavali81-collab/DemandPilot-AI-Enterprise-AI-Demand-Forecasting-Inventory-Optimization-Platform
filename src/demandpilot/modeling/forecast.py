"""Recursive horizon forecasting; no future actual sales are used."""
import json
from functools import lru_cache
import numpy as np
import pandas as pd
import lightgbm as lgb
from demandpilot.config import MODEL_FILE,META_FILE
from demandpilot.features.build_features import FEATURES,row_features

@lru_cache(maxsize=1)
def load_bundle():
    if not MODEL_FILE.exists() or not META_FILE.exists():
        raise FileNotFoundError("Run python scripts/bootstrap.py first")
    return lgb.Booster(model_file=str(MODEL_FILE)),json.loads(META_FILE.read_text())

def predict_series(model,metadata,history,product_id,store_id,days=30,future_price=None,promotional_days=None):
    if not 1<=days<=90:
        raise ValueError("days must be between 1 and 90")
    if product_id not in metadata["products"] or store_id not in metadata["stores"]:
        raise ValueError("Unknown product or store")
    subset=history.loc[(history.product_id==product_id)&(history.store_id==store_id)].sort_values("date")
    if len(subset)<28:
        raise ValueError("Insufficient historical observations")
    values=subset.units_sold.astype(float).tolist()
    last=pd.Timestamp(subset.date.max())
    price=float(future_price if future_price is not None else subset.iloc[-1].price)
    if price<=0:
        raise ValueError("future_price must be positive")
    promos=set(promotional_days or [])
    rows=[]
    for step in range(1,days+1):
        when=last+pd.Timedelta(days=step)
        row=row_features(values,when,price,int(when.date().isoformat() in promos),
            metadata["products"][product_id],metadata["stores"][store_id],pd.Timestamp(metadata["origin"]))
        if metadata.get("selected_model")=="seasonal_naive":
            y=values[-7]
        elif isinstance(model,lgb.Booster):
            y=float(model.predict(pd.DataFrame([row])[FEATURES],num_threads=1)[0])
        else:
            y=float(model.predict(pd.DataFrame([row])[FEATURES])[0])
        y=max(0.,float(y))
        values.append(y)
        width=1.645*metadata["residual_std"]*np.sqrt(step)
        rows.append({"date":when.strftime("%Y-%m-%d"),"predicted_units":round(y,2),
            "lower_approx":round(max(0.,y-width),2),"upper_approx":round(y+width,2)})
    return pd.DataFrame(rows)
