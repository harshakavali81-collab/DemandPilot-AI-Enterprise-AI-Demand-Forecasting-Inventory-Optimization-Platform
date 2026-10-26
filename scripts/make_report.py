"""Generate SVG figures and an EDA summary from the bootstrap-generated data."""
import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from demandpilot.config import SALES_FILE,REPORTS

def main():
    if not SALES_FILE.exists():
        raise SystemExit("Run python scripts/bootstrap.py first")
    sales=pd.read_csv(SALES_FILE,parse_dates=["date"])
    figs=REPORTS/"figures"
    figs.mkdir(parents=True,exist_ok=True)
    daily=sales.groupby("date").units_sold.sum()
    fig,ax=plt.subplots(figsize=(10,4))
    daily.rolling(7).mean().plot(ax=ax,label="7-day sales average")
    ax.set(title="Synthetic daily retail sales",xlabel="Date",ylabel="Units per day")
    ax.legend()
    fig.tight_layout()
    fig.savefig(figs/"sales_trend.svg")
    plt.close(fig)
    vol=sales.groupby("product_id").units_sold.sum().sort_values()
    fig,ax=plt.subplots(figsize=(8,4))
    vol.plot.barh(ax=ax)
    ax.set(title="Synthetic sales by SKU",xlabel="Units sold")
    fig.tight_layout()
    fig.savefig(figs/"product_volume.svg")
    plt.close(fig)
    data={"dataset":"synthetic","start":str(sales.date.min().date()),
          "end":str(sales.date.max().date()),"rows":len(sales),
          "total_units":int(sales.units_sold.sum())}
    (REPORTS/"eda_summary.json").write_text(json.dumps(data,indent=2)+"\n")
    print(data)
if __name__=="__main__":
    main()
