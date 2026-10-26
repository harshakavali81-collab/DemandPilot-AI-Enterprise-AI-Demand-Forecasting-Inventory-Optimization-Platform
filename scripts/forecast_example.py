"""Predict one sample series in process and calculate a reorder action."""
import pandas as pd
from demandpilot.config import SALES_FILE,STOCK_FILE
from demandpilot.modeling.forecast import load_bundle,predict_series
from demandpilot.inventory.optimizer import recommend
def main():
    model,meta=load_bundle()
    sales=pd.read_csv(SALES_FILE,parse_dates=["date"])
    item=pd.read_csv(STOCK_FILE).iloc[0]
    lead=int(item.lead_time_days)
    pred=predict_series(model,meta,sales,str(item.product_id),str(item.store_id),lead+7)
    rec=recommend(pred.predicted_units.tolist(),int(item.on_hand),int(item.on_order),
        int(item.backorders),lead,7,meta["residual_std"],
        float(item.service_level),float(item.unit_cost))
    print(pred.to_string(index=False))
    print(rec.to_dict())
if __name__=="__main__":
    main()
