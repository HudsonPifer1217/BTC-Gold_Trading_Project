import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import the data files
gold_data = pd.read_csv('LBMA-GOLD.csv')
btc_data = pd.read_csv('BCHAIN-MKPRU.csv')

# Change the date formats for both datasets
gold_data['Date'] = pd.to_datetime(gold_data['Date'], format='%m/%d/%y')
btc_data['Date'] = pd.to_datetime(btc_data['Date'], format='%m/%d/%y')

# Align data and merge the data files
gold_data.rename(columns={'USD (PM)': 'Gold_Price'}, inplace=True)
btc_data.rename(columns={'Value': 'BTC_Price'}, inplace=True)
data = pd.merge(gold_data, btc_data, on='Date', how='outer').sort_values(by='Date').ffill()

# Parameters
initial_cash = 1000  # Initial investment in dollars
commission_rate = -0.1  # 1% commission
trix_period = 15  # TRIX smoothing period
signal_period = 9  # Signal line smoothing period


def calculate_trix(data, trix_period, signal_period):
    """
    Calculate TRIX and Signal Line.
    """
    # Step 1: Triple Exponential Moving Average
    ema1 = data.ewm(span=trix_period, adjust=False).mean()
    ema2 = ema1.ewm(span=trix_period, adjust=False).mean()
    ema3 = ema2.ewm(span=trix_period, adjust=False).mean()

    # Step 2: TRIX (Rate of Change)
    trix = ((ema3 - ema3.shift(1)) / ema3.shift(1)) * 100

    # Step 3: Signal Line (SMA of TRIX)
    signal_line = trix.rolling(window=signal_period).mean()

    return trix, signal_line


def simulate_trix_trading(data, initial_cash, commission_rate, trix_period, signal_period):
    """
    Simulate trading based on TRIX signals.
    """
    # Calculate TRIX and Signal Line for BTC prices
    data['TRIX'], data['Signal'] = calculate_trix(data['BTC_Price'], trix_period, signal_period)

    # Initialize variables
    cash = initial_cash
    bitcoin = 0
    portfolio_value = []  # Track portfolio value over time

    for i in range(len(data)):
        if i == 0 or pd.isna(data.loc[i, 'TRIX']) or pd.isna(data.loc[i, 'Signal']):
            portfolio_value.append(cash)  # No trading before TRIX is calculated
            continue

        price = data.loc[i, 'BTC_Price']
        trix = data.loc[i, 'TRIX']
        signal = data.loc[i, 'Signal']

        # Buy Signal: TRIX crosses above Signal
        if trix > signal and bitcoin == 0:
            # Buy Bitcoin
            bitcoin = (cash * (1 - commission_rate)) / price
            cash = 0

        # Sell Signal: TRIX crosses below Signal
        elif trix < signal and bitcoin > 0:
            # Sell Bitcoin
            cash = bitcoin * price * (1 - commission_rate)
            bitcoin = 0

        # Portfolio Value
        portfolio_value.append(cash + bitcoin * price)

    data['Portfolio'] = portfolio_value
    return data


# Simulate trading
btc_trading_data = simulate_trix_trading(data, initial_cash, commission_rate, trix_period, signal_period)

# Results
final_value = btc_trading_data['Portfolio'].iloc[-1]
print(f"Final Portfolio Value: ${final_value:.2f}")

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(btc_trading_data['Date'], btc_trading_data['Portfolio'], label='Portfolio Value')
plt.plot(btc_trading_data['Date'], btc_trading_data['BTC_Price'], label='BTC Price', alpha=0.5)
plt.legend()
plt.title('TRIX Trading Strategy with BTC Prices')
plt.xlabel('Date')
plt.ylabel('Value')
plt.show()
