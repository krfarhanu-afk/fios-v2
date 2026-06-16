import os
import requests
import json
import time
from datetime import datetime, timedelta

# --- CONFIGURATION ---
# It's better to load secrets from a secure place, but for simplicity, we use Streamlit's secrets handling
# which requires the app to be run in a Streamlit context. For this script, we'll assume secrets are available.
# In a real-world scenario, you might use python-dotenv or a similar library.
try:
    from streamlit.errors import StreamlitSecretNotFoundError
    import streamlit as st
    FINNHUB_API_KEY = st.secrets["FINNHUB_API_KEY"]
    FMP_API_KEY = st.secrets["FMP_API_KEY"]
except (ImportError, StreamlitSecretNotFoundError):
    import toml
    secrets_path = os.path.join(os.path.dirname(__file__), '..', '.streamlit', 'secrets.toml')
    with open(secrets_path, 'r') as f:
        secrets = toml.load(f)
    FINNHUB_API_KEY = secrets.get("FINNHUB_API_KEY")
    FMP_API_KEY = secrets.get("FMP_API_KEY")


FINNHUB_BASE_URL = "https://finnhub.io/api/v1"
FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"
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

def get_from_fmp(endpoint, params):
    """Generic function to fetch data from FMP."""
    params['apikey'] = FMP_API_KEY
    try:
        response = requests.get(f"{FMP_BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from FMP: {e}")
        return None

def save_to_cache(filename, data):
    """Saves data to a JSON file in the cache directory."""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    with open(os.path.join(CACHE_DIR, filename), 'w') as f:
        json.dump(data, f, indent=2)

# --- CORE FUNCTIONS ---
def get_company_profile(ticker):
    """
    Fetches a company profile, trying Finnhub first and FMP as a fallback.
    """
    # Try Finnhub first
    profile_data = get_from_finnhub("stock/profile2", {'symbol': ticker})
    if profile_data:
        # Finnhub returns a dictionary, we can adapt it to our schema
        profile = {
            "ticker": profile_data.get("ticker"),
            "name": profile_data.get("name"),
            "exchange": profile_data.get("exchange"),
            "sector": profile_data.get("finnhubIndustry"),
            "market_cap": profile_data.get("marketCapitalization"),
            "website": profile_data.get("weburl"),
            "logo_url": profile_data.get("logo")
        }
        return profile

    # Fallback to FMP
    fmp_data = get_from_fmp(f"profile/{ticker}", {})
    if fmp_data:
        # FMP returns a list of profiles
        fmp_profile = fmp_data[0]
        profile = {
            "ticker": fmp_profile.get("symbol"),
            "name": fmp_profile.get("companyName"),
            "exchange": fmp_profile.get("exchangeShortName"),
            "sector": fmp_profile.get("sector"),
            "industry": fmp_profile.get("industry"),
            "market_cap": fmp_profile.get("mktCap"),
            "description": fmp_profile.get("description"),
            "website": fmp_profile.get("website"),
            "logo_url": fmp_profile.get("image")
        }
        return profile

    return None

def get_daily_prices(ticker, days=365):
    """
    Fetches daily price history for a ticker, trying Finnhub first and FMP as a fallback.
    """
    # --- Finnhub Attempt ---
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    unix_start = int(time.mktime(start_date.timetuple()))
    unix_end = int(time.mktime(end_date.timetuple()))

    price_data = get_from_finnhub("stock/candle", {
        'symbol': ticker,
        'resolution': 'D',
        'from': unix_start,
        'to': unix_end
    })

    if price_data and price_data.get('s') == 'ok':
        history = []
        for i in range(len(price_data['t'])):
            history.append({
                "date": datetime.fromtimestamp(price_data['t'][i]).strftime('%Y-%m-%d'),
                "open": price_data['o'][i],
                "high": price_data['h'][i],
                "low": price_data['l'][i],
                "close": price_data['c'][i],
                "volume": price_data['v'][i]
            })
        return {"ticker": ticker, "history": history}

    # --- FMP Fallback ---
    fmp_start_date = start_date.strftime('%Y-%m-%d')
    fmp_end_date = end_date.strftime('%Y-%m-%d')
    fmp_data = get_from_fmp(f"historical-price-full/{ticker}", {'from': fmp_start_date, 'to': fmp_end_date})

    if fmp_data and 'historical' in fmp_data:
        history = []
        for item in fmp_data['historical']:
            history.append({
                "date": item.get('date'),
                "open": item.get('open'),
                "high": item.get('high'),
                "low": item.get('low'),
                "close": item.get('close'),
                "volume": item.get('volume')
            })
        return {"ticker": ticker, "history": history}

    return None

if __name__ == "__main__":
    # Example usage for testing
    TICKERS = ["AAPL", "MSFT", "NVDA", "SPY", "QQQ"]

    for ticker in TICKERS:
        print(f"Fetching data for {ticker}...")

        # Fetch and save profile
        profile = get_company_profile(ticker)
        if profile:
            save_to_cache(f"{ticker}_profile.json", profile)
            print(f"  - Profile for {ticker} saved.")
        else:
            print(f"  - Failed to fetch profile for {ticker}.")

        # Fetch and save daily prices
        prices = get_daily_prices(ticker)
        if prices:
            save_to_cache(f"{ticker}_daily_prices.json", prices)
            print(f"  - Daily prices for {ticker} saved.")
        else:
            print(f"  - Failed to fetch daily prices for {ticker}.")
        
        # To avoid hitting API rate limits
        time.sleep(1)