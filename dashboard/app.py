"""Interactive demand forecasting and inventory planning dashboard."""
import os
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

API=os.getenv("DEMANDPILOT_API_URL","http://localhost:8000").rstrip("/")
st.set_page_config(page_title="DemandPilot AI",page_icon="📈",layout="wide")
st.title("📈 DemandPilot AI")
st.caption("Demand forecasting • inventory planning • SYNTHETIC demo data")

@st.cache_data(ttl=60)
def get(path):
    r=requests.get(f"{API}{path}",timeout=45)
    r.raise_for_status()
    return r.json()
def post(path,body):
    r=requests.post(f"{API}{path}",json=body,timeout=45)
    r.raise_for_status()
    return r.json()

try:
    catalog=get("/catalog")
    metrics=get("/metrics")
except (requests.RequestException,ValueError) as exc:
    st.error(f"API unavailable: {exc}")
    st.code("python scripts/bootstrap.py\nuvicorn demandpilot.api.main:app --reload")
    st.stop()

page=st.sidebar.radio("Navigate",["Overview","Demand Forecast","Inventory Planner","Model Evaluation"])
st.sidebar.info("Simulation only: not operational purchasing advice.")

if page=="Overview":
    alerts=get("/inventory/alerts")
    df=pd.DataFrame(alerts)
    a,b,c,d=st.columns(4)
    a.metric("SKU-store combinations",len(df))
    b.metric("High stockout risks",int((df.risk_level=="HIGH").sum()))
    c.metric("Recommended units",f"{int(df.recommended_order.sum()):,}")
    d.metric("Indicative order cost",f"₹{df.estimated_order_cost.sum():,.0f}")
    top=df.sort_values("estimated_stockout_probability",ascending=False).head(16).copy()
    top["label"]=top.store_id+" / "+top.product_name
    fig=px.bar(top,x="estimated_stockout_probability",y="label",orientation="h",
       color="risk_level",labels={"estimated_stockout_probability":"Approx. stockout probability","label":"SKU"})
    fig.update_layout(yaxis={"categoryorder":"total ascending"},height=550)
    st.plotly_chart(fig,use_container_width=True)
    st.dataframe(df,use_container_width=True,hide_index=True)
    st.download_button("Download inventory report",df.to_csv(index=False).encode(),
                       file_name="demandpilot_inventory.csv",mime="text/csv")

elif page=="Demand Forecast":
    items={f"{x['store_id']} • {x['product_name']} ({x['product_id']})":x for x in catalog}
    choice=items[st.selectbox("Store / Product",list(items))]
    days=st.select_slider("Horizon (days)",options=[7,14,30,60,90],value=30)
    if st.button("Generate forecast",type="primary"):
        try:
            out=post("/forecast",{"product_id":choice["product_id"],
                                 "store_id":choice["store_id"],"days":days})
            df=pd.DataFrame(out["forecast"])
            st.metric("Expected units",f"{out['total_forecast_units']:,.1f}")
            fig=go.Figure()
            fig.add_trace(go.Scatter(x=df.date,y=df.upper_approx,mode="lines",
                                     line={"width":0},showlegend=False))
            fig.add_trace(go.Scatter(x=df.date,y=df.lower_approx,mode="lines",
                                     fill="tonexty",fillcolor="rgba(59,130,246,0.13)",
                                     line={"width":0},name="Heuristic range"))
            fig.add_trace(go.Scatter(x=df.date,y=df.predicted_units,mode="lines+markers",
                                     name="Forecast"))
            st.plotly_chart(fig,use_container_width=True)
            st.caption(out["uncertainty_note"])
            st.dataframe(df,use_container_width=True,hide_index=True)
            st.download_button("Download forecast",df.to_csv(index=False).encode(),
                               file_name="demandpilot_forecast.csv",mime="text/csv")
        except requests.RequestException as exc:
            st.error(str(exc))

elif page=="Inventory Planner":
    st.subheader("What-if reorder calculator")
    st.caption("Uses user-entered constant demand assumptions, not live inventory.")
    one,two,three=st.columns(3)
    with one:
        demand=st.number_input("Daily demand",0.,10000.,20.)
        on_hand=st.number_input("On-hand",0,1000000,80)
        incoming=st.number_input("Incoming units",0,1000000,0)
    with two:
        lead=st.number_input("Lead time (days)",1,90,5)
        review=st.number_input("Review period (days)",1,90,7)
        backorders=st.number_input("Backorders",0,1000000,0)
    with three:
        std=st.number_input("Daily error standard deviation",0.,10000.,5.)
        service=st.slider("Service target",.5,.999,.95)
        cost=st.number_input("Unit cost (₹)",0.,1000000.,300.)
    if st.button("Calculate reorder",type="primary"):
        try:
            r=post("/inventory/recommend",{"forecast":[demand]*(lead+review),
               "on_hand":on_hand,"on_order":incoming,"backorders":backorders,
               "lead_time_days":lead,"review_period_days":review,
               "residual_std":std,"service_level":service,"unit_cost":cost})
            a,b,c=st.columns(3)
            a.metric("Recommended units",r["recommended_order"])
            b.metric("Reorder point",r["reorder_point"])
            c.metric("Indicative cost",f"₹{r['estimated_order_cost']:,.0f}")
            st.json(r)
        except requests.RequestException as exc:
            st.error(str(exc))
else:
    st.subheader("Chronological holdout evaluation — synthetic data")
    df=pd.DataFrame([{"split":split,"model":name,**vals}
          for split in ("validation","test") for name,vals in metrics[split].items()])
    st.write(f"**Model chosen on validation:** {metrics['selected_model']}")
    st.dataframe(df,hide_index=True,use_container_width=True)
    st.plotly_chart(px.bar(df,x="split",y="wape_pct",color="model",barmode="group"),
                    use_container_width=True)
    st.warning(metrics["model_limitations"]+". "+metrics["uncertainty_note"])
