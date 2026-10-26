import numpy as np
import pandas as pd
from demandpilot.data.generate import generate
from demandpilot.features.build_features import catalog_maps
from demandpilot.modeling.forecast import predict_series
from demandpilot.modeling.evaluate import metrics
class FakeBooster:
    def predict(self,x):return np.full(len(x),12.5)

def test_future_forecast_recursive_and_bounded():
    sales,_=generate(days=110)
    meta={**catalog_maps(sales),"selected_model":"lightgbm","residual_std":2.}
    df=predict_series(FakeBooster(),meta,sales,"P101","HYD01",30)
    assert len(df)==30
    assert (df.predicted_units>=0).all()
    assert df.date.iloc[0]==(sales.date.max()+pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    assert df.predicted_units.iloc[-1]==12.5

def test_metrics_zero_error():
    result=metrics([1,2,3],[1,2,3])
    assert result["wape_pct"]==result["mae"]==result["rmse"]==0
