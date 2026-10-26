import pytest
from demandpilot.inventory.optimizer import recommend

def test_sensible_reorder():
    r=recommend([10]*12,on_hand=20,lead_time_days=5,review_period_days=7,
                residual_std=0,unit_cost=100)
    assert r.reorder_point==50
    assert r.recommended_order==100
    assert r.estimated_order_cost==10000
    assert r.risk_level=="HIGH"

def test_incoming_stock_reduces_order():
    a=recommend([10]*12,5,lead_time_days=5,review_period_days=7)
    b=recommend([10]*12,5,on_order=100,lead_time_days=5,review_period_days=7)
    assert b.recommended_order<a.recommended_order

def test_forecast_must_cover_lead_review():
    with pytest.raises(ValueError,match="cover"):
        recommend([10]*3,10,lead_time_days=4,review_period_days=7)
