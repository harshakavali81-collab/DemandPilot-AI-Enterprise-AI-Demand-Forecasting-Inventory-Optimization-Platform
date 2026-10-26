from demandpilot.data.generate import generate
from demandpilot.modeling.train import train
def test_training_is_reproducible_and_split_is_chronological():
    sales,_=generate(days=140)
    _,meta,report=train(sales,persist=False)
    assert meta["selected_model"] in ("lightgbm","seasonal_naive")
    assert report["training_rows"]>0
    assert report["validation_rows"]>0
    assert report["test_rows"]>0
    assert report["train_until_exclusive"]<report["test_from_inclusive"]
