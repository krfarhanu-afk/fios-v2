import streamlit as st
import pandas as pd
import json
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Equities", page_icon="📈", layout="wide")

# --- DATA LOADING ---
CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'cache')
TICKERS = ["AAPL", "MSFT", "NVDA", "SPY", "QQQ"]
TICKER_TO_CIK = {
    "AAPL": "0000320193",
    "MSFT": "0000789019",
    "NVDA": "0001045810",
}

def load_cache_data(filename):
    """Loads data from a JSON file in the cache directory."""
    filepath = os.path.join(CACHE_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return None # File is empty or corrupted
    return None

# --- UI LAYOUT ---
st.title("Equity Analysis")

# Ticker Selector
ticker = st.selectbox("Select a ticker", TICKERS)

st.divider()

# Load data for the selected ticker
profile_data = load_cache_data(f"{ticker}_profile.json")
price_data = load_cache_data(f"{ticker}_daily_prices.json")
news_data = load_cache_data(f"{ticker}_news.json")
filings_data = load_cache_data(f"{ticker}_filings.json")
cik = TICKER_TO_CIK.get(ticker)

# --- Profile Header ---
if profile_data and profile_data.get("name"):
    col1, col2 = st.columns([1, 4])
    with col1:
        if profile_data.get("logo_url"):
            st.image(profile_data["logo_url"], width=100)
        else:
            st.write(" ") # Placeholder for alignment
    with col2:
        st.header(profile_data["name"])
        st.write(f"{profile_data.get('exchange', 'N/A')}: {profile_data.get('ticker', 'N/A')}")
        st.write(f"**Sector:** {profile_data.get('sector', 'N/A')}")
else:
    st.header(f"Data for {ticker}")
    st.warning("Company profile data is not available.")

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["Summary", "News", "Filings"])

with tab1:
    st.subheader("Price Chart")
    if price_data and price_data.get("history"):
        price_df = pd.DataFrame(price_data["history"])
        if not price_df.empty and 'date' in price_df.columns:
            price_df = price_df.set_index("date")
            st.line_chart(price_df["close"])
        else:
            st.info("Price data is available but in an unexpected format.")
    else:
        st.info("Daily price data is not available.")

    st.subheader("Company Description")
    if profile_data and profile_data.get("description"):
        st.write(profile_data["description"])
    else:
        st.info("Company description is not available.")

with tab2:
    st.subheader("Recent News")
    if news_data and news_data.get("articles"):
        for article in news_data["articles"]:
            st.write(f"**[{article.get('headline', 'No Headline')}]({article.get('url', '#')})** - {article.get('source', 'N/A')}")
            st.write(article.get('summary', 'No summary available.'))
            st.caption(f"Published: {article.get('published_at', 'N/A')}")
            st.markdown("---")
    else:
        st.info("News data is not available.")

with tab3:
    st.subheader("Recent SEC Filings")
    if filings_data and filings_data.get("filings"):
        for filing in filings_data["filings"]:
            st.write(f"**Form:** {filing.get('form', 'N/A')} - {filing.get('primary_doc_description', 'No description')}")
            st.write(f"**Filed:** {filing.get('filing_date', 'N/A')} | **Report Date:** {filing.get('report_date', 'N/A')}")
            # The SEC provides a URL to the filing's index page.
            # A more advanced implementation could parse this page to find the direct document link.
            filing_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{filing.get('accession_number', '').replace('-', '')}/{filing.get('primary_document')}"
            st.write(f"[View Filing]({filing_url})")
            st.markdown("---")
    else:
        st.info("SEC filings data is not available for this ticker.")