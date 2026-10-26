"""Pydantic API request validation."""
from datetime import date
from pydantic import BaseModel,Field,model_validator

class ForecastRequest(BaseModel):
    product_id:str
    store_id:str
    days:int=Field(default=30,ge=1,le=90)
    future_price:float|None=Field(default=None,gt=0)
    promotional_days:list[date]=Field(default_factory=list)

class InventoryRequest(BaseModel):
    forecast:list[float]=Field(min_length=1)
    on_hand:int=Field(ge=0)
    on_order:int=Field(default=0,ge=0)
    backorders:int=Field(default=0,ge=0)
    lead_time_days:int=Field(default=5,ge=1,le=90)
    review_period_days:int=Field(default=7,ge=1,le=90)
    residual_std:float=Field(default=4.0,ge=0)
    service_level:float=Field(default=.95,ge=.5,le=.999)
    unit_cost:float=Field(default=0.0,ge=0)
    @model_validator(mode="after")
    def check_forecast_length(self):
        if len(self.forecast)<self.lead_time_days+self.review_period_days:
            raise ValueError("forecast must cover lead_time_days + review_period_days")
        return self
