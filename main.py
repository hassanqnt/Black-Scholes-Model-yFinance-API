"""
Black-Scholes Option Pricing Model 2025 Yahoo-Compatible
Note: Data no longer available as of 2026 due to soft IP blocks
Warning: yFinance API utilises scraped data which is a compliance risk

Assumptions:
- European options
- No dividends
- Constant risk-free rate
"""

import sys
import time
import numpy as np
import yfinance as yf
from scipy.stats import norm

def get_price_history(ticker, period="1y", interval="1d", retries=3):
    for _ in range(retries):
        try:
            tk = yf.Ticker(ticker)
            data = tk.history(period=period, interval=interval)

            if not data.empty:
                return data

        except Exception:
            pass

        time.sleep(2)

    raise RuntimeError(f"Yahoo Finance unavailable for ticker: {ticker}")


# Volatility Estimation

def historical_volatility(prices):
    log_returns = np.log(prices / prices.shift(1)).dropna()
    return log_returns.std() * np.sqrt(252)


# User Inputs

def get_inputs():
    symbol = input("Stock/Ticker: ").upper()

    try:
        stock_data = get_price_history(symbol)
    except RuntimeError as e:
        print(e)
        sys.exit(1)

    S = round(stock_data["Close"].iloc[-1], 2)
    print(f"Underlying Price: {S}")

    # Risk-free rate (10Y Treasury Yield)
    try:
        rate_data = get_price_history("^TNX", period="3mo")
        R = rate_data["Close"].iloc[-1] / 100
    except RuntimeError:
        print("Failed to retrieve risk-free rate.")
        sys.exit(1)

    sigma = historical_volatility(stock_data["Close"])

    # Strike
    while True:
        try:
            K = float(input("Strike Price: "))
            if K > 0:
                break
        except ValueError:
            pass
        print("Invalid strike price.")

    # Maturity
    while True:
        try:
            T = float(input("Time to Maturity (years, e.g. 0.5): "))
            if T > 0:
                break
        except ValueError:
            pass
        print("Invalid maturity.")

    # Option type
    while True:
        option_type = input("Option Type (C/P): ").upper()
        if option_type in ("C", "P"):
            break
        print("Invalid option type.")

    return symbol, S, K, T, R, sigma, option_type


# Black-Scholes Formula


def black_scholes_price(S, K, T, R, sigma, option_type):
    d1 = (np.log(S / K) + (R + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "C":
        return S * norm.cdf(d1) - K * np.exp(-R * T) * norm.cdf(d2)
    else:
        return K * np.exp(-R * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def main():
    symbol, S, K, T, R, sigma, option_type = get_inputs()

    price = black_scholes_price(S, K, T, R, sigma, option_type)

    print("\n--- Black-Scholes Result ---")
    print(f"Ticker: {symbol}")
    print(f"Option Type: {'Call' if option_type == 'C' else 'Put'}")
    print(f"Option Price: {price:.2f}")
    print(f"Annualized Volatility: {sigma:.2%}")
    print(f"Risk-Free Rate: {R:.2%}")


if __name__ == "__main__":
    main()