import os
import sys
import time

# Add the parent directory to the Python path to allow imports from the 'services' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.market_data import get_company_profile, get_daily_prices, save_to_cache
from services.sec_edgar import get_sec_filings
from services.ai_summary import generate_ai_brief
import json

# --- CONFIGURATION ---
TICKERS = ["AAPL", "MSFT", "NVDA", "SPY", "QQQ"]
CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'cache')

def load_cache_data(filename):
    """Loads data from a JSON file in the cache directory."""
    filepath = os.path.join(CACHE_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from {filename}")
                return None
    return None

def refresh_all_data():
    """
    Iterates through all tickers and refreshes their profile and daily price data.
    """
    print("--- Starting Daily Data Refresh ---")
    
    for ticker in TICKERS:
        print(f"Fetching data for {ticker}...")

        # --- Refresh Company Profile ---
        try:
            profile = get_company_profile(ticker)
            if profile:
                save_to_cache(f"{ticker}_profile.json", profile)
                print(f"  - Profile for {ticker} saved.")
            else:
                print(f"  - Failed to fetch profile for {ticker}. Using existing cache if available.")
        except Exception as e:
            print(f"  - An error occurred while fetching profile for {ticker}: {e}")

        # --- Refresh Daily Prices ---
        try:
            prices = get_daily_prices(ticker)
            if prices:
                save_to_cache(f"{ticker}_daily_prices.json", prices)
                print(f"  - Daily prices for {ticker} saved.")
            else:
                print(f"  - Failed to fetch daily prices for {ticker}. Using existing cache if available.")
        except Exception as e:
            print(f"  - An error occurred while fetching prices for {ticker}: {e}")
        
        # --- Refresh SEC Filings ---
        try:
            filings = get_sec_filings(ticker)
            if filings:
                save_to_cache(f"{ticker}_filings.json", filings)
                print(f"  - SEC filings for {ticker} saved.")
            else:
                print(f"  - Failed to fetch SEC filings for {ticker}.")
        except Exception as e:
            print(f"  - An error occurred while fetching SEC filings for {ticker}: {e}")

        # Respect API rate limits
        print("--- Waiting to avoid hitting API rate limits ---")
        time.sleep(1)

    print("--- Generating AI Summaries ---")
    for ticker in TICKERS:
        print(f"Generating AI summary for {ticker}...")
        profile = load_cache_data(f"{ticker}_profile.json")
        news = load_cache_data(f"{ticker}_news.json")
        filings = load_cache_data(f"{ticker}_filings.json")

        if profile: # Only generate a brief if we have at least the profile
            brief = generate_ai_brief(ticker, profile, news, filings)
            if brief:
                save_to_cache(f"{ticker}_ai_brief.json", {"brief": brief})
                print(f"  - AI brief for {ticker} saved.")
            else:
                print(f"  - Failed to generate AI brief for {ticker}.")
        else:
            print(f"  - Skipping AI brief for {ticker} due to missing profile data.")

    print("--- Daily Data Refresh Complete ---")

if __name__ == "__main__":
    refresh_all_data()