"""All target-day features are calculated from prior observations only."""
import numpy as np
import pandas as pd

FEATURES = ["product_code","store_code","day_of_week","month","is_weekend","time_index",
            "price","promo","lag_1","lag_7","lag_14","lag_28","rolling_7","rolling_28","rolling_std_7"]
CATEGORICAL = ["product_code","store_code","day_of_week","month"]

def catalog_maps(sales: pd.DataFrame) -> dict:
    return {"products": {s:i for i,s in enumerate(sorted(sales.product_id.unique()))},
            "stores": {s:i for i,s in enumerate(sorted(sales.store_id.unique()))},
            "origin": str(sales.date.min().date())}

def row_features(history: list[float], when: pd.Timestamp, price: float, promo: int,
                 product_code: int, store_code: int, origin: pd.Timestamp) -> dict:
    if len(history) < 28:
        raise ValueError("At least 28 historical observations required")
    return {"product_code":product_code,"store_code":store_code,
            "day_of_week":when.weekday(),"month":when.month,
            "is_weekend":int(when.weekday()>=5),"time_index":(when-origin).days,
            "price":float(price),"promo":int(promo),
            "lag_1":history[-1],"lag_7":history[-7],
            "lag_14":history[-14],"lag_28":history[-28],
            "rolling_7":float(np.mean(history[-7:])),
            "rolling_28":float(np.mean(history[-28:])),
            "rolling_std_7":float(np.std(history[-7:],ddof=0))}

def make_features(sales: pd.DataFrame, maps: dict) -> pd.DataFrame:
    groups=[]
    origin=pd.Timestamp(maps["origin"])
    for (store,product),group in sales.groupby(["store_id","product_id"]):
        group=group.sort_values("date")
        values=group.units_sold.tolist()
        rows=[]
        for i in range(28,len(group)):
            item=group.iloc[i]
            feat=row_features(values[:i],pd.Timestamp(item.date),item.price,int(item.promo),
                              maps["products"][product],maps["stores"][store],origin)
            feat.update({"date":pd.Timestamp(item.date),"store_id":store,
                         "product_id":product,"target":float(values[i])})
            rows.append(feat)
        groups.append(pd.DataFrame(rows))
    if not groups or all(x.empty for x in groups):
        raise ValueError("Insufficient sales history")
    return pd.concat(groups,ignore_index=True).sort_values("date").reset_index(drop=True)
