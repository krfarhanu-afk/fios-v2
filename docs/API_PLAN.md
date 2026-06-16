# FIOS API Plan

This document details the external APIs, endpoints, and fallback strategies for FIOS V1.

## Guiding Principles

1.  **Cost-Effectiveness:** Prioritize free or low-cost API tiers.
2.  **Redundancy:** Have a fallback provider for critical data points where possible.
3.  **Simplicity:** Use simple, well-documented REST APIs.

---

## Data Providers

| Data Type             | Primary Provider | Fallback Provider | Notes                                          |
| --------------------- | ---------------- | ----------------- | ---------------------------------------------- |
| Company Profile       | Finnhub          | FMP               | FMP has more detailed profiles but is secondary. |
| Daily Prices          | Finnhub          | FMP               | Both are reliable for end-of-day prices.       |
| News                  | Finnhub          | GNews             | Finnhub is preferred for ticker-specific news. |
| SEC Filings           | SEC EDGAR API    | None              | The official source; no fallback needed.       |
| Macro (GDP, CPI)      | FMP              | None              | FMP provides this data in a clean format.      |
| AI Summary            | OpenAI           | None              | GPT-4 or latest model available.               |

---

## Endpoint Plan

### 1. Finnhub

-   **API Key:** `FINNHUB_API_KEY`
-   **Base URL:** `https://finnhub.io/api/v1`

-   **Company Profile:**
    -   Endpoint: `/stock/profile2`
    -   Params: `symbol={TICKER}`

-   **Daily Prices (Stock Candles):**
    -   Endpoint: `/stock/candle`
    -   Params: `symbol={TICKER}`, `resolution=D`, `from={START_DATE}`, `to={END_DATE}`

-   **News:**
    -   Endpoint: `/company-news`
    -   Params: `symbol={TICKER}`, `from={START_DATE}`, `to={END_DATE}`

### 2. Financial Modeling Prep (FMP)

-   **API Key:** `FMP_API_KEY`
-   **Base URL:** `https://financialmodelingprep.com/api/v3`

-   **Company Profile (Fallback):**
    -   Endpoint: `/profile/{TICKER}`

-   **Macro - GDP:**
    -   Endpoint: `/economic/gdp`

-   **Macro - CPI:**
    -   Endpoint: `/economic/cpi`

### 3. SEC EDGAR API

-   **API Key:** None (requires a `User-Agent` header)
-   **Base URL:** `https://data.sec.gov/submissions`

-   **Filings:**
    -   Endpoint: `/CIK{CIK_NUMBER}.json`
    -   Note: Requires a mapping from Ticker to CIK.

### 4. GNews (Fallback)

-   **API Key:** `GNEWS_API_KEY`
-   **Base URL:** `https://gnews.io/api/v4`

-   **News:**
    -   Endpoint: `/search`
    -   Params: `q={TICKER}`, `lang=en`

### 5. OpenAI

-   **API Key:** `OPENAI_API_KEY`
-   **Base URL:** `https://api.openai.com/v1`

-   **AI Summary:**
    -   Endpoint: `/chat/completions`
    -   Model: `gpt-4` (or preferred model)
    -   Body: See `AI_PROMPT.md` for the prompt structure.

---

## Fallback Rules

-   If a primary API call fails (e.g., status code 500, timeout), the script will attempt **one** retry.
-   If the retry fails, it will proceed to the fallback provider.
-   If the fallback provider also fails, the script will log the error and continue, leaving the corresponding cache file unchanged.
-   A failure of the SEC EDGAR or OpenAI APIs will be logged, and the process will continue without that data for the day.