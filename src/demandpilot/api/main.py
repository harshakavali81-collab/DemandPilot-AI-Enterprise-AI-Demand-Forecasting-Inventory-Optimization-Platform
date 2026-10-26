"""REST endpoints for forecasts and inventory planning; Swagger at /docs."""
import json
from functools import lru_cache
import pandas as pd
from fastapi import FastAPI,HTTPException,Query
from demandpilot.config import SALES_FILE,STOCK_FILE,METRICS_FILE
from demandpilot.api.schemas import ForecastRequest,InventoryRequest
from demandpilot.modeling.forecast import load_bundle,predict_series
from demandpilot.inventory.optimizer import recommend
from demandpilot.storage.database import record_forecast

app=FastAPI(title="DemandPilot AI",version="1.0.0",
    description="Synthetic-data decision-support demo, NOT a production ERP")

@lru_cache(maxsize=1)
def load_data():
    if not SALES_FILE.exists() or not STOCK_FILE.exists():
        raise FileNotFoundError("Demo data missing: run python scripts/bootstrap.py")
    return pd.read_csv(SALES_FILE,parse_dates=["date"]),pd.read_csv(STOCK_FILE)

def state():
    try:
        model,meta=load_bundle()
        sales,stock=load_data()
        return model,meta,sales,stock
    except (FileNotFoundError,OSError,ValueError) as exc:
        raise HTTPException(status_code=503,detail=str(exc)) from exc

@app.get("/health")
def health():
    return {"status":"ok","trained":METRICS_FILE.exists(),"data_source":"synthetic retail simulation"}

@app.get("/catalog")
def catalog():
    _,_,_,stock=state()
    return stock[["store_id","product_id","product_name"]].to_dict(orient="records")

@app.post("/forecast")
def forecast(req:ForecastRequest):
    model,meta,sales,_=state()
    try:
        forecast=predict_series(model,meta,sales,req.product_id,req.store_id,
            req.days,req.future_price,[str(x) for x in req.promotional_days])
    except ValueError as exc:
        raise HTTPException(status_code=422,detail=str(exc)) from exc
    total=round(float(forecast.predicted_units.sum()),2)
    record_forecast(req.store_id,req.product_id,req.days,total)
    return {"product_id":req.product_id,"store_id":req.store_id,
            "horizon_days":req.days,"total_forecast_units":total,
            "model":meta["selected_model"],"source":"synthetic",
            "forecast":forecast.to_dict(orient="records"),
            "uncertainty_note":"Approximate, uncalibrated heuristic ranges"}

@app.post("/inventory/recommend")
def inventory_recommend(req:InventoryRequest):
    try:
        return recommend(**req.model_dump()).to_dict()
    except ValueError as exc:
        raise HTTPException(status_code=422,detail=str(exc)) from exc

@app.get("/inventory/alerts")
def inventory_alerts(review_period_days:int=Query(7,ge=1,le=30)):
    model,meta,sales,stock=state()
    alerts=[]
    for _,item in stock.iterrows():
        lead=int(item.lead_time_days)
        pred=predict_series(model,meta,sales,str(item.product_id),
                            str(item.store_id),lead+review_period_days)
        r=recommend(pred.predicted_units.tolist(),int(item.on_hand),int(item.on_order),
            int(item.backorders),lead,review_period_days,float(meta["residual_std"]),
            float(item.service_level),float(item.unit_cost))
        alerts.append({"product_id":item.product_id,"store_id":item.store_id,
                       "product_name":item.product_name,**r.to_dict()})
    return sorted(alerts,key=lambda x:x["estimated_stockout_probability"],reverse=True)

@app.get("/metrics")
def metrics():
    if not METRICS_FILE.exists():
        raise HTTPException(status_code=503,detail="Train demo model first")
    return json.loads(METRICS_FILE.read_text())
