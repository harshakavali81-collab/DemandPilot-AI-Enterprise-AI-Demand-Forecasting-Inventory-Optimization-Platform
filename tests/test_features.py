import pandas as pd
import pytest
from demandpilot.data.generate import generate
from demandpilot.data.validate import validate_sales
from demandpilot.features.build_features import catalog_maps,make_features,row_features

def test_features_do_not_include_target():
    sales,_=generate(days=110)
    frame=make_features(sales,catalog_maps(sales))
    historic=sales[(sales.store_id=="HYD01")&(sales.product_id=="P101")].sort_values("date")
    row=frame[(frame.store_id=="HYD01")&(frame.product_id=="P101")].iloc[0]
    assert row.lag_1==historic.iloc[27].units_sold
    assert row.lag_7==historic.iloc[21].units_sold
    assert row.target==historic.iloc[28].units_sold

def test_rejects_duplicate_daily_data():
    sales,_=generate(days=100)
    with pytest.raises(ValueError,match="Duplicate"):
        validate_sales(pd.concat([sales,sales.iloc[[0]]],ignore_index=True))

def test_need_28_historical_days():
    with pytest.raises(ValueError):
        row_features([1]*27,pd.Timestamp("2026-01-01"),100,0,0,0,
                     pd.Timestamp("2025-01-01"))
