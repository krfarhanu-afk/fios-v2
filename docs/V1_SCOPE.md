# FIOS V1 Scope

This document defines the features included in and excluded from the first version of the Financial Intelligence Operating System (FIOS).

## Included Features

The goal of V1 is to deliver a minimal, valuable, and functional daily briefing tool.

- **Tickers:** Analysis will be limited to the following 5 tickers:
  - `AAPL` (Apple Inc.)
  - `MSFT` (Microsoft Corporation)
  - `NVDA` (NVIDIA Corporation)
  - `SPY` (SPDR S&P 500 ETF Trust)
  - `QQQ` (Invesco QQQ Trust)

- **Today Dashboard:** A main landing page summarizing the most critical updates for the monitored tickers.

- **Ticker Detail Pages:** Individual pages for each ticker, providing more in-depth data, news, and filing information.

- **Macro Page:** A dedicated page for high-level macroeconomic indicators and news.

- **AI Brief:** A daily, AI-generated summary that synthesizes key market movements, news, and events.

- **Research Notes:** A simple interface for users to jot down their own thoughts and research findings.

- **Authentication:** A basic, single-password login mechanism to protect access.

## Excluded Features

To ensure a focused and timely V1 release, the following features are explicitly out of scope:

- **User Accounts:** No multi-user system; a single password will be shared.
- **Customizable Ticker Lists:** The initial 5 tickers are fixed.
- **Real-Time Data:** All data will be fetched and cached on a periodic basis (daily/weekly), not streamed in real-time.
- **Advanced Analytics:** No complex charting, backtesting, or quantitative analysis tools.
- **Brokerage Integration:** No ability to link to or execute trades with brokerage accounts.
- **Alerts & Notifications:** No automated email or push notifications.
- **Team/Collaboration Features:** No sharing or multi-user annotation.