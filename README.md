# FIOS - Financial Intelligence Overview System

## What FIOS Does

FIOS (Financial Intelligence Overview System) is a V1 prototype designed to provide a quick, cache-first overview of key financial data. Its primary goal is to make financial intelligence accessible daily, even if some external APIs are unavailable or rate-limited.

**Key Features:**
- **Cache-First Data Loading:** Prioritizes reading data from local JSON cache files for speed and resilience.
- **AI Daily Briefs:** Generates concise AI-powered summaries of market and company news.
- **Tracked Tickers:** Focuses on `AAPL`, `MSFT`, `NVDA`, `SPY`, `QQQ`.
- **SEC EDGAR Filings:** Integrates free and reliable SEC filings data.
- **Password Protection:** Secures access to the application with a login.
- **Local Research Vault:** A placeholder for storing and managing personal research notes.

## Installation

To set up FIOS locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/krfarhanu-afk/fios-v2.git
    cd fios-v2/fios
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    ```
3.  **Activate the virtual environment:**
    *   **Windows:**
        ```bash
        .venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run Locally

1.  **Ensure your virtual environment is activated.**
2.  **Set up your secrets:** Create a file named `.streamlit/secrets.toml` in the `fios` directory (next to `app.py`). Refer to `.streamlit/secrets.example.toml` for the required keys.
3.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    The application will open in your web browser, usually at `http://localhost:8501`.

## Required Secrets

FIOS requires the following secrets, which should be placed in `.streamlit/secrets.toml`:

```toml
LOGIN_USERNAME = "your_username" # e.g., "admin"
LOGIN_PASSWORD = "your_password" # e.g., "password"
FINNHUB_API_KEY = "your_finnhub_api_key"
FMP_API_KEY = "your_fmp_api_key"
OPENAI_API_KEY = "your_openai_api_key"
```
**Note:** A `secrets.example.toml` file is provided for reference. **Do not commit your `secrets.toml` file to GitHub.**

## Current Limitations

*   `services/news.py` and `scripts/refresh_weekly.py` are currently empty placeholders.
*   Price and news cache files may be sparse or empty due to free API endpoint restrictions.
*   SPY and QQQ (ETFs) do not have SEC filing support, which is expected.
*   The application is designed for deployment on Streamlit Community Cloud, not Vercel.

## Cache Files

For this V1 prototype, cache files located in `data/cache/` are committed to the repository to facilitate easy deployment and testing on Streamlit Cloud. This ensures that the application has some data to display even if API calls fail during deployment.