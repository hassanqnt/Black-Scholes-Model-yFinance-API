📌 Project Overview & Data Design
This project implements a Black Scholes option pricing model for European options, using historical price data to estimate annualised volatility and a U.S.
Treasury based risk free rate. The codebase is structured with explicit validation, defensive error handling, and moduler components to support future
extensions such as Greeks, Monte Carlo pricing, and implied volatility estimation.


Data Source Considerations
This project does not rely on Yahoo Finance / yfinance. While commonly used for prototyping, Yahoo Finance is not an official or supported
market data API and its endpoints are undocumented and increasingly unstable. Automated access is frequently blocked or degraded, resulting in malformed
responses, empty datasets, misleading errors (e.g. “symbol may be delisted”), and non deterministic behavior that varies by network, IP address,
and TLS/SSL configuration (notably on macOS environments).

Compliance & Reproducibility
Yahoo Finance data is obtained via scraping rather than licensed distribution, which introduces compliance, legal, and auditability risks in professional or
regulated contexts. Data provenance cannot be guaranteed, historical results are not reproducible over time and silent data changes undermine research integrity.
For these reasons, scraped data sources such as Yahoo Finance are avoided in institutional quantitative workflows.

Forward-Looking Design
The project is data provider agnostic by design and will be updated to use a reliable, officially supported market data API in future iterations.
Planned improvements include migration to a licensed data provider, optional local data caching for deterministic backtesting and expanded analytical features.
