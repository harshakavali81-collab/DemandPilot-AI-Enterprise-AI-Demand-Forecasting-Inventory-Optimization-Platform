"""Generate demo data, train model and initialize database in one command."""
from demandpilot.data.generate import generate
from demandpilot.config import SALES_FILE,STOCK_FILE,DATA
from demandpilot.modeling.train import train
from demandpilot.storage.database import initialize

def main():
    sales,stock=generate()
    DATA.mkdir(parents=True,exist_ok=True)
    sales.to_csv(SALES_FILE,index=False)
    stock.to_csv(STOCK_FILE,index=False)
    initialize(sales,stock)
    _,meta,metrics=train(sales)
    print(f"Demo ready: {len(sales)} synthetic sales rows, {len(stock)} simulated inventory records")
    print(f"Selected model: {meta['selected_model']}")
    print(f"Test WAPE: {metrics['test'][meta['selected_model']]['wape_pct']}% — synthetic data only")
if __name__=="__main__":
    main()
