from fastapi.testclient import TestClient
from demandpilot.api.main import app
client=TestClient(app)

def test_health_endpoint():
    r=client.get("/health")
    assert r.status_code==200
    assert r.json()["data_source"].startswith("synthetic")

def test_validation_blocks_too_long_horizon():
    r=client.post("/forecast",json={"product_id":"P101","store_id":"HYD01","days":999})
    assert r.status_code==422

def test_inventory_endpoint():
    r=client.post("/inventory/recommend",json={"forecast":[10]*12,
        "on_hand":20,"lead_time_days":5,"review_period_days":7,"residual_std":0})
    assert r.status_code==200
    assert r.json()["recommended_order"]==100

def test_inventory_rejects_missing_days():
    r=client.post("/inventory/recommend",json={"forecast":[10,12],"on_hand":20})
    assert r.status_code==422
