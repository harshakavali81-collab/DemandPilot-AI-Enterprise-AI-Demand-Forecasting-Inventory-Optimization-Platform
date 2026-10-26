"""MAE/RMSE/WAPE metrics."""
import numpy as np

def metrics(actual,pred):
    a,p=np.asarray(actual,dtype=float),np.asarray(pred,dtype=float)
    if not len(a) or len(a)!=len(p):
        raise ValueError("Expected equal nonempty arrays")
    err=a-p
    return {"mae":round(float(np.mean(abs(err))),4),
            "rmse":round(float(np.sqrt(np.mean(err**2))),4),
            "wape_pct":round(float(100*np.sum(abs(err))/max(np.sum(abs(a)),1e-9)),3)}
