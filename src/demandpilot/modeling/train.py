"""Chronological model selection and out-of-time test (synthetic data)."""
import json
from datetime import datetime,timezone
import numpy as np
import pandas as pd
import lightgbm as lgb
from demandpilot.config import SALES_FILE,MODEL_FILE,META_FILE,METRICS_FILE,ARTIFACTS
from demandpilot.data.validate import validate_sales
from demandpilot.features.build_features import FEATURES,CATEGORICAL,catalog_maps,make_features
from demandpilot.modeling.evaluate import metrics

def fit_model(frame):
    model=lgb.LGBMRegressor(n_estimators=180,learning_rate=.055,num_leaves=15,
          min_child_samples=28,reg_lambda=2.,verbosity=-1,random_state=42,n_jobs=2)
    model.fit(frame[FEATURES],frame["target"],categorical_feature=CATEGORICAL)
    return model

def train(sales:pd.DataFrame,persist:bool=True):
    sales=validate_sales(sales)
    maps=catalog_maps(sales)
    frame=make_features(sales,maps)
    dates=sorted(frame.date.unique())
    if len(dates)<90:
        raise ValueError("At least 90 target dates needed")
    train_end=dates[int(len(dates)*.70)]
    val_end=dates[int(len(dates)*.85)]
    first=frame[frame.date<train_end]
    val=frame[(frame.date>=train_end)&(frame.date<val_end)]
    fit_all=frame[frame.date<val_end]
    test=frame[frame.date>=val_end]
    if any(x.empty for x in (first,val,fit_all,test)):
        raise ValueError("Empty chronological partition")
    candidate=fit_model(first)
    val_ml=np.maximum(candidate.predict(val[FEATURES]),0)
    val_results={"lightgbm":metrics(val.target,val_ml),
                 "seasonal_naive":metrics(val.target,val.lag_7)}
    winner=min(val_results,key=lambda k:val_results[k]["wape_pct"])
    final_model=fit_model(fit_all)
    test_ml=np.maximum(final_model.predict(test[FEATURES]),0)
    test_naive=test.lag_7.to_numpy()
    tests={"lightgbm":metrics(test.target,test_ml),
           "seasonal_naive":metrics(test.target,test_naive)}
    residuals=np.asarray(test.target,float)-(test_naive if winner=="seasonal_naive" else test_ml)
    residual_std=max(1.,float(np.std(residuals)))
    report={"dataset":"synthetic (not real retail transactions)",
        "training_rows":len(first),"validation_rows":len(val),"test_rows":len(test),
        "train_until_exclusive":str(pd.Timestamp(train_end).date()),
        "test_from_inclusive":str(pd.Timestamp(val_end).date()),
        "validation":val_results,"test":tests,"selected_model":winner,
        "selection_rule":"lowest validation WAPE; test not used for selection",
        "uncertainty_note":"Uncalibrated heuristic intervals; not validated coverage",
        "model_limitations":"Forecasts observed sales, not censored latent demand; synthetic data"}
    meta={**maps,"selected_model":winner,"residual_std":round(residual_std,5),
          "trained_at_utc":datetime.now(timezone.utc).isoformat(),
          "last_sales_date":str(sales.date.max().date()),"model_version":"demo-v1"}
    if persist:
        ARTIFACTS.mkdir(parents=True,exist_ok=True)
        final_model.booster_.save_model(str(MODEL_FILE))
        META_FILE.write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
        METRICS_FILE.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    return final_model,meta,report

def main():
    if not SALES_FILE.exists():
        raise SystemExit("Run python scripts/bootstrap.py first")
    _,_,report=train(pd.read_csv(SALES_FILE))
    print(json.dumps(report,indent=2))
if __name__=="__main__":
    main()
