import requests
import json
import os

# --- CONFIGURATION ---
# The SEC requires a User-Agent header that includes your company name and email.
# This is to identify who is making the requests.
# Please replace the placeholder values with your actual information.
COMPANY_NAME = "Farhan"
CONTACT_EMAIL = "kr.farhan.u@gmail.com"
HEADERS = {'User-Agent': f'{COMPANY_NAME} {CONTACT_EMAIL}'}

CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'cache')

def get_sec_filings(ticker):
    """
    Fetches recent SEC filings for a given ticker.
    Note: The SEC EDGAR API requires a CIK number. This function assumes a mapping
    or another function would be available to convert a ticker to a CIK.
    For this initial version, we will use a hardcoded CIK for Apple as an example.
    """
    # This is a simplified example. A real implementation would need a robust
    # way to map tickers to CIKs (Central Index Key).
    ticker_to_cik = {
        "AAPL": "0000320193",
        "MSFT": "0000789019",
        "NVDA": "0001045810",
        # SPY and QQQ are ETFs and don't have the same kind of company filings.
        # We will handle them gracefully.
    }

    cik = ticker_to_cik.get(ticker)
    if not cik:
        print(f"No CIK found for ticker: {ticker}")
        return None

    try:
        # The API returns data in JSON format.
        response = requests.get(f"https://data.sec.gov/submissions/CIK{cik}.json", headers=HEADERS)
        response.raise_for_status()
        data = response.json()

        # We are interested in the 'filings' and 'recent' data.
        recent_filings = data.get('filings', {}).get('recent', {})
        
        # The data is returned with keys like 'accessionNumber', 'filingDate', 'form', etc.
        # We can reformat this into a more readable list of dictionaries.
        filings = []
        for i in range(len(recent_filings.get('accessionNumber', []))):
            filings.append({
                "accession_number": recent_filings['accessionNumber'][i],
                "filing_date": recent_filings['filingDate'][i],
                "report_date": recent_filings['reportDate'][i],
                "form": recent_filings['form'][i],
                "primary_document": recent_filings['primaryDocument'][i],
                "primary_doc_description": recent_filings['primaryDocDescription'][i],
            })
        
        return {"ticker": ticker, "filings": filings}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching SEC filings for {ticker}: {e}")
        return None

def save_to_cache(filename, data):
    """Saves data to a JSON file in the cache directory."""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    with open(os.path.join(CACHE_DIR, filename), 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    # Example usage for testing
    TICKERS = ["AAPL", "MSFT", "NVDA", "SPY", "QQQ"]

    for ticker in TICKERS:
        print(f"Fetching SEC filings for {ticker}...")
        filings = get_sec_filings(ticker)
        if filings:
            save_to_cache(f"{ticker}_filings.json", filings)
            print(f"  - SEC filings for {ticker} saved.")
        else:
            print(f"  - Failed to fetch SEC filings for {ticker}.")