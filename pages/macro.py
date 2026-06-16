import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Macro", page_icon="🌍", layout="wide")

# --- FAKE DATA ---
FAKE_MACRO_INDICATORS = {
  "gdp_quarterly": [
    {"date": "2022-Q4", "value": 26.47},
    {"date": "2023-Q1", "value": 26.83},
    {"date": "2023-Q2", "value": 27.06},
    {"date": "2023-Q3", "value": 27.64}
  ],
  "cpi_monthly": [
    {"date": "2023-06", "value": 3.0},
    {"date": "2023-07", "value": 3.2},
    {"date": "2023-08", "value": 3.7},
    {"date": "2023-09", "value": 3.7}
  ],
  "interest_rate_monthly": [
    {"date": "2023-07", "value": 5.50},
    {"date": "2023-08", "value": 5.50},
    {"date": "2023-09", "value": 5.50},
    {"date": "2023-10", "value": 5.50}
  ]
}

# --- UI LAYOUT ---
st.title("Macroeconomic Dashboard")
st.write("Key indicators influencing the market environment.")

st.divider()

# --- METRICS ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label="GDP (Quarterly, Trillions)",
        value=f"${FAKE_MACRO_INDICATORS['gdp_quarterly'][-1]['value']}",
        delta=f"${round(FAKE_MACRO_INDICATORS['gdp_quarterly'][-1]['value'] - FAKE_MACRO_INDICATORS['gdp_quarterly'][-2]['value'], 2)}"
    )
with col2:
    st.metric(
        label="CPI (Monthly, YoY %)",
        value=f"{FAKE_MACRO_INDICATORS['cpi_monthly'][-1]['value']}%",
        delta=f"{round(FAKE_MACRO_INDICATORS['cpi_monthly'][-1]['value'] - FAKE_MACRO_INDICATORS['cpi_monthly'][-2]['value'], 2)}%"
    )
with col3:
    st.metric(
        label="Fed Funds Rate",
        value=f"{FAKE_MACRO_INDICATORS['interest_rate_monthly'][-1]['value']}%"
    )

st.divider()

# --- CHARTS ---
st.subheader("Historical Trends")

# GDP Chart
gdp_df = pd.DataFrame(FAKE_MACRO_INDICATORS["gdp_quarterly"]).set_index("date")
st.line_chart(gdp_df, use_container_width=True)
st.caption("US GDP, Quarterly")

# CPI Chart
cpi_df = pd.DataFrame(FAKE_MACRO_INDICATORS["cpi_monthly"]).set_index("date")
st.line_chart(cpi_df, use_container_width=True)
st.caption("US CPI, Monthly Year-over-Year")