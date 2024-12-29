from organize_data import *
from testing_LMA_and_SMA import *
import matplotlib.pyplot as plt




# Define the best SMA and LMA combination
best_sma = 45
best_lma = 120
'''

# Calculate moving averages for both BTC and Gold
data['BTC_SMA'] = data['BTC_Price'].rolling(window=best_sma).mean()
data['BTC_LMA'] = data['BTC_Price'].rolling(window=best_lma).mean()
data['Gold_SMA'] = data['Gold_Price'].rolling(window=best_sma).mean()
data['Gold_LMA'] = data['Gold_Price'].rolling(window=best_lma).mean()

# Drop NaNs
temp_data = data.dropna().reset_index(drop=True)

# Initialize portfolio
cash, btc, gold = 1000, 0, 0  # Initial portfolio
buy_sell_log = []  # To log trades
portfolio_values = []  # To track portfolio value over time

# Add a trading threshold to reduce excessive trades
threshold = 0.03  # 1% price difference required to trigger a trade

# Add holding period and refined logic
holding_period = 10  # Minimum days to hold before selling
last_btc_trade = -holding_period
last_gold_trade = -holding_period

for i in range(len(temp_data) - 1):
    current_date = temp_data.loc[i, 'Date']
    btc_price = temp_data.loc[i, 'BTC_Price']
    gold_price = temp_data.loc[i, 'Gold_Price']
    btc_sma = temp_data.loc[i, 'BTC_SMA']
    btc_lma = temp_data.loc[i, 'BTC_LMA']
    gold_sma = temp_data.loc[i, 'Gold_SMA']
    gold_lma = temp_data.loc[i, 'Gold_LMA']

    # Calculate expected profits with a higher threshold
    btc_expected_profit = (btc_sma - btc_price * (1 + threshold + 0.02)) / btc_price if btc_sma > btc_lma else 0
    gold_expected_profit = (gold_sma - gold_price * (1 + threshold + 0.01)) / gold_price if gold_sma > gold_lma else 0

    # Determine the best asset to buy
    if btc_expected_profit > gold_expected_profit and cash > 0 and btc_expected_profit > threshold:
        btc += (cash * 0.98) / btc_price  # 2% commission
        cash = 0
        last_btc_trade = i
        buy_sell_log.append((current_date, 'Buy', 'BTC', btc_price))
    elif gold_expected_profit > btc_expected_profit and cash > 0 and gold_expected_profit > threshold:
        gold += (cash * 0.99) / gold_price  # 1% commission
        cash = 0
        last_gold_trade = i
        buy_sell_log.append((current_date, 'Buy', 'Gold', gold_price))

    # Sell logic with holding period
    if btc_expected_profit < -threshold and btc > 0 and (i - last_btc_trade) > holding_period:
        cash += btc * btc_price * 0.98  # 2% commission
        btc = 0
        last_btc_trade = i
        buy_sell_log.append((current_date, 'Sell', 'BTC', btc_price))
    if gold_expected_profit < -threshold and gold > 0 and (i - last_gold_trade) > holding_period:
        cash += gold * gold_price * 0.99  # 1% commission
        gold = 0
        last_gold_trade = i
        buy_sell_log.append((current_date, 'Sell', 'Gold', gold_price))

    # Update portfolio value
    portfolio_value = cash + (btc * btc_price) + (gold * gold_price)
    portfolio_values.append((current_date, portfolio_value)'''

'''
#calculate moving avgs:
data['Gold_SMA'] = data['Gold_Price'].rolling(window=sma).mean()
data['Gold_LMA'] = data['Gold_Price'].rolling(window=lma).mean()
data['BTC_SMA'] = data['BTC_Price'].rolling(window=sma).mean()
data['BTC_LMA'] = data['BTC_Price'].rolling(window=lma).mean()

#drop empty days and reset portfolio:
temp_data = data.dropna().reset_index(drop=True)
cash, gold, btc = 1000, 0, 0
buy_sell_log = []
portfolio_values = []
#Stimulate trading for given SMA/ LMA combination:
for i in range(len(temp_data)-1):
    current_date = temp_data.loc[i, 'Date']
    btc_price = temp_data.loc[i, 'BTC_Price']
    gold_price = temp_data.loc[i, 'Gold_Price']
    gold_sma = temp_data.loc[i, 'Gold_SMA']
    gold_lma = temp_data.loc[i, 'Gold_LMA']
    btc_sma = temp_data.loc[i, 'BTC_SMA']
    btc_lma = temp_data.loc[i, 'BTC_LMA']


    ## TRADING USING GOLDEN AND DEATH CROSS

    #trading logic for gold:
    if gold_sma > gold_lma:    #Buy Gold
        if cash > 0:   ## if there is cash...
            gold += (cash * 0.99)/ gold_price   # 1% commission
            cash = 0    ## go all in
            buy_sell_log.append((current_date, 'Buy', 'Gold', gold_price))
    elif gold_sma < gold_lma and gold > 0:   # Sell Gold
        cash += gold * gold_price * 0.99    # 1% commission
        gold = 0  #sell all the gold
        buy_sell_log.append((current_date, 'Sell', 'Gold', gold_price))

    #trading logic for BTC:
    if btc_sma > btc_lma:  # Buy Bitcoin
        if cash > 0:
            btc += (cash * 0.98) / btc_price  # 2% commission
            cash = 0
            buy_sell_log.append((current_date, 'Buy', 'BTC', btc_price))
    elif btc_sma < btc_lma and btc > 0:  # Sell Bitcoin
        cash += btc * btc_price * 0.98  # 2% commission
        btc = 0
        buy_sell_log.append((current_date, 'Sell', 'BTC', btc_price))

    final_value = cash + (gold * temp_data.iloc[-1]['Gold_Price']) + (btc * temp_data.iloc[-1]['BTC_Price'])
    results.append((sma, lma, final_value))
'''


# Extract dates and portfolio values
#dates, portfolio_values = zip(*results)
'''
# Plot portfolio value over time
plt.figure(figsize=(14, 8))
plt.plot(dates, portfolio_values, label='Portfolio Value', color='purple')
plt.title(f"Portfolio Value Over Time (SMA={best_sma}, LMA={best_lma})", fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Portfolio Value (USD)', fontsize=14)
plt.grid()
plt.legend()

# Plot BTC and Gold trades
for trade in buy_sell_log:
    if trade[1] == 'Buy' and trade[2] == 'BTC':
        plt.axvline(trade[0], color='green', linestyle='--', alpha=0.6, label='BTC Buy' if 'BTC Buy' not in plt.gca().get_legend_handles_labels()[1] else None)
    elif trade[1] == 'Sell' and trade[2] == 'BTC':
        plt.axvline(trade[0], color='red', linestyle='--', alpha=0.6, label='BTC Sell' if 'BTC Sell' not in plt.gca().get_legend_handles_labels()[1] else None)
    elif trade[1] == 'Buy' and trade[2] == 'Gold':
        plt.axvline(trade[0], color='blue', linestyle='--', alpha=0.6, label='Gold Buy' if 'Gold Buy' not in plt.gca().get_legend_handles_labels()[1] else None)
    elif trade[1] == 'Sell' and trade[2] == 'Gold':
        plt.axvline(trade[0], color='orange', linestyle='--', alpha=0.6, label='Gold Sell' if 'Gold Sell' not in plt.gca().get_legend_handles_labels()[1] else None)



plt.tight_layout()
plt.legend()
#plt.show()

'''

import matplotlib.pyplot as plt
import pandas as pd

# Assuming `data` is your dataset and already loaded.

# Define SMA and LMA
sma = 1
lma = 60

# Calculate SMA and LMA for gold
data['Gold_SMA'] = data['Gold_Price'].rolling(window=sma).mean()
data['Gold_LMA'] = data['Gold_Price'].rolling(window=lma).mean()

# Drop rows with NaN values
data = data.dropna().reset_index(drop=True)

# Initialize portfolio and signal lists
cash, gold = 1000, 0
buy_signals = []
sell_signals = []

# Trading logic with buy/sell signal tracking
for i in range(len(data) - 1):
    current_gold_price = data.loc[i, 'Gold_Price']
    gold_sma = data.loc[i, 'Gold_SMA']
    gold_lma = data.loc[i, 'Gold_LMA']

    # Buy Gold
    if gold_sma > gold_lma and cash > 0:
        gold += (cash * 0.99) / current_gold_price  # 1% commission
        cash = 0
        buy_signals.append((data.loc[i, 'Date'], current_gold_price))
    # Sell Gold
    elif gold_sma < gold_lma and gold > 0:
        cash += gold * current_gold_price * 0.99  # 1% commission
        gold = 0
        sell_signals.append((data.loc[i, 'Date'], current_gold_price))

# Convert buy and sell signals to separate lists for plotting
buy_dates, buy_prices = zip(*buy_signals) if buy_signals else ([], [])
sell_dates, sell_prices = zip(*sell_signals) if sell_signals else ([], [])

# Plot the Gold Price, SMA, LMA, and buy/sell signals
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['Gold_Price'], label='Gold Price', color='blue', zorder = 1)
plt.plot(data['Date'], data['Gold_SMA'], label=f'Gold SMA ({sma})', color='orange', linestyle='--', zorder = 2)
plt.plot(data['Date'], data['Gold_LMA'], label=f'Gold LMA ({lma})', color='green', linestyle='--', zorder = 2)

# Plot buy and sell signals
plt.scatter(buy_dates, buy_prices, label='Buy', color='green', marker='^', alpha=1, zorder=3)
plt.scatter(sell_dates, sell_prices, label='Sell', color='red', marker='v', alpha=1, zorder=3)

# Add labels, title, and legend
plt.title(f'Trades for gold with SMA={sma}, LMA={lma}')
plt.xlabel('Date')
plt.ylabel('Gold Price (USD)')
plt.legend()
plt.grid()
plt.tight_layout()

# Show the plot
plt.show()


# Define SMA and LMA
sma = 45
lma = 120

# Calculate SMA and LMA for BTC
data['BTC_SMA'] = data['BTC_Price'].rolling(window=sma).mean()
data['BTC_LMA'] = data['BTC_Price'].rolling(window=lma).mean()

# Drop rows with NaN values
data = data.dropna().reset_index(drop=True)

# Initialize portfolio and signal lists
cash, btc = 1000, 0
buy_signals = []
sell_signals = []

# Trading logic with buy/sell signal tracking
for i in range(len(data) - 1):
    current_btc_price = data.loc[i, 'BTC_Price']
    btc_sma = data.loc[i, 'BTC_SMA']
    btc_lma = data.loc[i, 'BTC_LMA']

    # Buy BTC
    if btc_sma > btc_lma and cash > 0:
        btc += (cash * 0.98) / current_btc_price  # 2% commission
        cash = 0
        buy_signals.append((data.loc[i, 'Date'], current_btc_price))
    # Sell BTC
    elif btc_sma < btc_lma and btc > 0:
        cash += btc * current_btc_price * 0.98  # 2% commission
        btc = 0
        sell_signals.append((data.loc[i, 'Date'], current_btc_price))

# Convert buy and sell signals to separate lists for plotting
buy_dates, buy_prices = zip(*buy_signals) if buy_signals else ([], [])
sell_dates, sell_prices = zip(*sell_signals) if sell_signals else ([], [])

# Plot the BTC Price, SMA, LMA, and buy/sell signals
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['BTC_Price'], label='BTC Price', color='blue', zorder = 1)
plt.plot(data['Date'], data['BTC_SMA'], label=f'BTC SMA ({sma})', color='orange', linestyle='--', zorder=2)
plt.plot(data['Date'], data['BTC_LMA'], label=f'BTC LMA ({lma})', color='green', linestyle='--', zorder=2)

# Plot buy and sell signals
plt.scatter(buy_dates, buy_prices, label='Buy', color='green', marker='^', alpha=1, zorder = 3)
plt.scatter(sell_dates, sell_prices, label='Sell', color='red', marker='v', alpha=1, zorder = 3)

# Add labels, title, and legend
plt.title(f'Trades for BTC with SMA={sma}, LMA={lma}')
plt.xlabel('Date')
plt.ylabel('BTC Price (USD)')
plt.legend()
plt.grid()
plt.tight_layout()

# Show the plot
#plt.show()

