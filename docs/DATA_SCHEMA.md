# FIOS Data Schema

This document outlines the structure of the JSON files stored in the `data/cache/` directory. These files serve as the primary data source for the Streamlit application.

## File Naming Convention

- **Equities:** `{TICKER}_{DATA_TYPE}.json` (e.g., `AAPL_profile.json`, `MSFT_news.json`)
- **Macro:** `macro_{DATA_TYPE}.json` (e.g., `macro_gdp.json`)
- **System:** `system_{DATA_TYPE}.json` (e.g., `system_last_refresh.json`)

---

## Equity Schemas

### 1. Profile (`{TICKER}_profile.json`)

Stores basic company information. Refreshed weekly.

```json
{
  "ticker": "AAPL",
  "name": "Apple Inc.",
  "exchange": "NASDAQ",
  "sector": "Technology",
  "industry": "Consumer Electronics",
  "market_cap": 3200000000000,
  "description": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide...",
  "website": "https://www.apple.com",
  "logo_url": "https://static.finnhub.io/logo/image.png"
}
```

### 2. Daily Prices (`{TICKER}_daily_prices.json`)

Stores daily open, high, low, close, and volume data for the past year. Refreshed daily.

```json
{
  "ticker": "AAPL",
  "history": [
    {
      "date": "2023-10-26",
      "open": 170.37,
      "high": 171.38,
      "low": 165.67,
      "close": 166.89,
      "volume": 35000000
    }
  ]
}
```

### 3. News (`{TICKER}_news.json`)

Stores recent news articles for a ticker. Refreshed daily.

```json
{
  "ticker": "AAPL",
  "articles": [
    {
      "source": "Bloomberg",
      "headline": "Apple Reports Record Quarterly Revenue",
      "summary": "Apple today announced financial results for its fiscal 2023 fourth quarter...",
      "url": "https://www.bloomberg.com/news/...",
      "published_at": "2023-10-26T20:00:00Z"
    }
  ]
}
```

### 4. SEC Filings (`{TICKER}_filings.json`)

Stores recent SEC filings. Refreshed daily.

```json
{
  "ticker": "AAPL",
  "filings": [
    {
      "type": "10-K",
      "filed_at": "2023-10-27T08:00:00Z",
      "url": "https://www.sec.gov/Archives/edgar/data/..."
    }
  ]
}
```

---

## Macro Schemas

### 1. Economic Indicators (`macro_indicators.json`)

Stores key macroeconomic data points. Refreshed weekly.

```json
{
  "gdp_quarterly": [
    {"date": "2023-Q3", "value": 27.64},
    {"date": "2023-Q2", "value": 27.06}
  ],
  "cpi_monthly": [
    {"date": "2023-09", "value": 3.7},
    {"date": "2023-08", "value": 3.7}
  ],
  "interest_rate_monthly": [
    {"date": "2023-10", "value": 5.50}
  ]
}
```

---

## System Schemas

### 1. Last Refresh (`system_last_refresh.json`)

Tracks when the data caches were last updated.

```json
{
  "daily_last_run": "2023-10-27T04:00:00Z",
  "weekly_last_run": "2023-10-22T04:00:00Z"
}
```

### 2. AI Brief (`system_ai_brief.json`)

Stores the latest AI-generated daily summary.

```json
{
  "generated_at": "2023-10-27T05:00:00Z",
  "brief": "Market overview: The S&P 500 closed down 0.5% as concerns over interest rates persist. Key Movers: NVDA saw a 3% gain on positive AI chip news. Noteworthy Events: Apple's latest 10-K filing shows increased R&D spending..."
}
```