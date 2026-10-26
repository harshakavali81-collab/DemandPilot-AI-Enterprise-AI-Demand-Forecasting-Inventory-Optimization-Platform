"""Periodic-review reorder calculations using approximate Normal demand errors."""
from dataclasses import dataclass,asdict
from math import ceil,erf,sqrt
from statistics import NormalDist
import numpy as np

@dataclass
class Recommendation:
    inventory_position:int
    demand_lead_time:float
    reorder_point:int
    order_up_to:int
    recommended_order:int
    estimated_stockout_probability:float
    risk_level:str
    estimated_order_cost:float
    def to_dict(self):return asdict(self)

def recommend(forecast:list[float],on_hand:int,on_order:int=0,backorders:int=0,
              lead_time_days:int=5,review_period_days:int=7,residual_std:float=4.,
              service_level:float=.95,unit_cost:float=0.):
    if not forecast or any(not np.isfinite(v) or v<0 for v in forecast):
        raise ValueError("Forecast must be finite and nonnegative")
    if min(on_hand,on_order,backorders,residual_std,unit_cost)<0:
        raise ValueError("Stock/error/cost must be nonnegative")
    if lead_time_days<1 or review_period_days<1:
        raise ValueError("Lead time and review period must be positive")
    if not .5<=service_level<=.999:
        raise ValueError("service_level must be in [0.5, 0.999]")
    if len(forecast)<lead_time_days+review_period_days:
        raise ValueError("Forecast must cover lead time plus review period")
    z=NormalDist().inv_cdf(service_level)
    lead=sum(forecast[:lead_time_days])
    protection=lead_time_days+review_period_days
    total=sum(forecast[:protection])
    point=ceil(lead+z*residual_std*sqrt(lead_time_days))
    target=ceil(total+z*residual_std*sqrt(protection))
    position=int(on_hand+on_order-backorders)
    sigma=residual_std*sqrt(lead_time_days)
    risk=(1. if position<lead else 0.) if sigma<=0 else .5*(1+erf((lead-position)/(sigma*sqrt(2))))
    qty=max(0,target-position) if position<=point else 0
    level="HIGH" if risk>=.5 else "MEDIUM" if risk>=.15 else "LOW"
    return Recommendation(position,round(lead,2),point,target,qty,round(risk,4),level,round(qty*unit_cost,2))
