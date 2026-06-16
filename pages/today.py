import streamlit as st
import os
import json

st.set_page_config(page_title="Today", page_icon="📅", layout="wide")

st.title("Today's Financial Brief")
st.write("A consolidated, AI-powered view of your tracked assets.")

# --- DATA LOADING ---
CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'cache')
TICKERS = ["AAPL", "MSFT", "NVDA", "SPY", "QQQ"]

def load_cache_data(filename):
    filepath = os.path.join(CACHE_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return None
    return None

# --- AI-POWERED BRIEFS ---
st.subheader("AI-Powered Daily Briefs")

for ticker in TICKERS:
    brief_data = load_cache_data(f"{ticker}_ai_brief.json")
    if brief_data and brief_data.get("brief"):
        with st.expander(f"**{ticker}** - AI Summary"):
            st.markdown(brief_data["brief"])
    else:
        with st.expander(f"**{ticker}** - AI Summary"):
            st.info("The AI brief for this ticker has not been generated yet. Please run the refresh script.")

# --- FOOTER ---
st.markdown("---")
st.write("FIOS - v1.0.0")