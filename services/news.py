import os
import requests
import json
from datetime import datetime, timedelta

# --- CONFIGURATION ---
try:
    from streamlit.errors import StreamlitSecretNotFoundError
    import streamlit as st
    FINNHUB_API_KEY = st.secrets["FINNHUB_API_KEY"]
except (ImportError, StreamlitSecretNotFoundError):
    import toml
    secrets_path = os.path.join(os.path.dirname(__file__), '..', '.streamlit', 'secrets.toml')
    with open(secrets_path, 'r') as f:
        secrets = toml.load(f)
    FINNHUB_API_KEY = secrets.get("FINNHUB_API_KEY")

FINNHUB_BASE_URL = "https://finnhub.io/api/v1"
CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'cache')

# --- HELPER FUNCTIONS ---
def get_from_finnhub(endpoint, params):
    """Generic function to fetch data from Finnhub."""
    params['token'] = FINNHUB_API_KEY
    try:
        response = requests.get(f"{FINNHUB_BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from Finnhub: {e}")
        return None

def save_to_cache(filename, data):
    """Saves data to a JSON file in the cache directory."""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    with open(os.path.join(CACHE_DIR, filename), 'w') as f:
        json.dump(data, f, indent=2)

# --- CORE FUNCTIONS ---
def get_company_news(ticker, days=7):
    """
    Fetches company news for a given ticker from Finnhub.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    news_data = get_from_finnhub("company-news", {
        'symbol': ticker,
        'from': start_date.strftime('%Y-%m-%d'),
        'to': end_date.strftime('%Y-%m-%d')
    })

    if news_data:
        # Filter out news without a valid image or summary
        filtered_news = [
            {
                "category": article.get("category"),
                "datetime": datetime.fromtimestamp(article.get("datetime")).isoformat(),
                "headline": article.get("headline"),
                "id": article.get("id"),
                "image": article.get("image"),
                "related": article.get("related"),
                "source": article.get("source"),
                "summary": article.get("summary"),
                "url": article.get("url")
            }
            for article in news_data if article.get("image") and article.get("summary") and article.get("url")
        ]
        return {"ticker": ticker, "news": filtered_news}
    return None

if __name__ == "__main__":
    # Example usage for testing
    TICKERS = ["AAPL", "MSFT", "NVDA", "SPY", "QQQ"]

    for ticker in TICKERS:
        print(f"Fetching news for {ticker}...")
        news = get_company_news(ticker)
        if news:
            save_to_cache(f"{ticker}_news.json", news)
            print(f"  - News for {ticker} saved.")
        else:
            print(f"  - Failed to fetch news for {ticker}.")