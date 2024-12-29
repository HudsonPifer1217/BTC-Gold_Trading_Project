import pandas as pd
import numpy as np


def calculate_wma(prices, window):
    """Calculate Weighted Moving Average (WMA)."""
    weights = np.arange(1, window + 1)
    return prices.rolling(window).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)


def calculate_ehma(prices, period):
    """Calculate Exponential Hull Moving Average (EHMA)."""
    if period < 2:
        raise ValueError("Period for EHMA must be greater than 1.")

    half_period = int(period / 2)
    sqrt_period = int(np.sqrt(period))

    wma_half = calculate_wma(prices, half_period)
    wma_full = calculate_wma(prices, period)

    hull_base = 2 * wma_half - wma_full
    ehma = calculate_wma(hull_base, sqrt_period)
    return ehma


def calculate_rsi(prices, period=14):
    """Calculate Relative Strength Index (RSI)."""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def integrate_ehma_with_rsi(data, period_btc, period_gold, rsi_period=14, threshold=0.01):
    """EHMA strategy with RSI filter."""
    data['BTC_EHMA'] = calculate_ehma(data['BTC_Price'], period_btc)
    data['Gold_EHMA'] = calculate_ehma(data['Gold_Price'], period_gold)
    data['BTC_RSI'] = calculate_rsi(data['BTC_Price'], rsi_period)
    data['Gold_RSI'] = calculate_rsi(data['Gold_Price'], rsi_period)

    cash, gold, btc = 1000, 0, 0

    for i in range(len(data) - 1):
        current_btc_price = data.loc[i, 'BTC_Price']
        current_gold_price = data.loc[i, 'Gold_Price']
        btc_ehma = data.loc[i, 'BTC_EHMA']
        gold_ehma = data.loc[i, 'Gold_EHMA']
        btc_rsi = data.loc[i, 'BTC_RSI']
        gold_rsi = data.loc[i, 'Gold_RSI']

        # Bitcoin trading with RSI filter
        if btc_ehma > current_btc_price * (1 + threshold) and btc_rsi < 30 and cash > 0:  # Buy BTC
            btc += (cash * 0.98) / current_btc_price
            cash = 0
        elif btc_ehma < current_btc_price * (1 - threshold) and btc_rsi > 70 and btc > 0:  # Sell BTC
            cash += btc * current_btc_price * 0.98
            btc = 0

        # Gold trading with RSI filter
        if gold_ehma > current_gold_price * (1 + threshold) and gold_rsi < 30 and cash > 0:  # Buy Gold
            gold += (cash * 0.99) / current_gold_price
            cash = 0
        elif gold_ehma < current_gold_price * (1 - threshold) and gold_rsi > 70 and gold > 0:  # Sell Gold
            cash += gold * current_gold_price * 0.99
            gold = 0

    final_value = cash + (gold * data.iloc[-1]['Gold_Price']) + (btc * data.iloc[-1]['BTC_Price'])
    return final_value


