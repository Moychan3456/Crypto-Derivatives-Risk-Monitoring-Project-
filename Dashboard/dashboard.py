import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Crypto Derivatives Risk Monitor", layout="wide")

st.title("Crypto Derivatives Risk Monitoring Dashboard")

# Load risk report
script_name = os.path.dirname(os.path.abspath(__file__))
file_path_risk = os.path.join(script_name, 'daily_risk_report_with_severity.csv')
risk_df = pd.read_csv(file_path_risk)

# -------- Desk Exposure Overview ----------
st.header("Desk Exposure Overview")

total_exposure = risk_df["Notional_Exposure"].sum()
st.metric("Total Desk Exposure ($)", f"{total_exposure:,.2f}")
desk_var = float(open(os.path.join(script_name, "desk_var.txt")).read())

col1, col2 = st.columns(2)

col1.metric("Desk 95% VaR ($)", f"{desk_var:,.2f}")


st.dataframe(risk_df)

# -------- Margin Utilization ----------
st.header("Margin Utilization")

st.bar_chart(risk_df.set_index("Trader")["Margin_Utilization"])

# -------- Risk Alerts ----------
st.header("Risk Alerts")

alerts = risk_df[
    (risk_df["Leverage_Flag"] == "BREACH") |
    (risk_df["Margin_Flag"] == "WARNING")
]

if alerts.empty:
    st.success("No risk breaches detected.")
else:
    st.error("Risk breaches detected!")
    st.dataframe(alerts)

st.header("Concentration Risk Monitor")

script_name = os.path.dirname(os.path.abspath(__file__))
file_path_asset = os.path.join(script_name, 'asset_concentration.csv')
file_path_trader = os.path.join(script_name, 'trader_concentration.csv')
asset_conc = pd.read_csv(file_path_asset)
trader_conc = pd.read_csv(file_path_trader)

st.subheader("Asset Concentration")
st.bar_chart(asset_conc.set_index("Asset")["Exposure_%"])

st.subheader("Trader Concentration")
st.bar_chart(trader_conc.set_index("Trader")["Exposure_%"])

st.header("Risk Severity Escalation Panel")

critical = risk_df[risk_df["Risk_Severity"] == "CRITICAL"]
warning = risk_df[risk_df["Risk_Severity"] == "WARNING"]

if not critical.empty:
    st.error("CRITICAL RISK POSITIONS")
    st.dataframe(critical)

if not warning.empty:
    st.warning("WARNING POSITIONS")
    st.dataframe(warning)

if critical.empty and warning.empty:
    st.success("All positions operating within risk tolerance.")
