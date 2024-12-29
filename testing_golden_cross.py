import pandas as pd
import numpy as np
from organize_data import *

# define ranges for SMA and LMA
sma_values = range(20, 101, 2)  # SMA from 20 to 100 days
lma_values = range(100, 251, 2)  # LMA from 100 to 250 da

results = []

for sma in sma_values:
    for lma in lma_values:
        if sma >= lma:  # Skip over invalid SMA and LMA combinations
            continue

        # Calculate moving averages
        data['Gold_SMA'] = data['Gold_Price'].rolling(window=sma).mean()
        data['Gold_LMA'] = data['Gold_Price'].rolling(window=lma).mean()
        data['BTC_SMA'] = data['BTC_Price'].rolling(window=sma).mean()
        data['BTC_LMA'] = data['BTC_Price'].rolling(window=lma).mean()

        # Drop rows with NaN values and reset portfolio
        temp_data = data.dropna().reset_index(drop=True)
        cash, gold, btc = 1000, 0, 0

        # Simulate trading for given SMA/LMA combination
        for i in range(1, len(temp_data) - 1):
            current_gold_price = temp_data.loc[i, 'Gold_Price']
            current_btc_price = temp_data.loc[i, 'BTC_Price']
            gold_sma = temp_data.loc[i, 'Gold_SMA']
            gold_lma = temp_data.loc[i, 'Gold_LMA']
            btc_sma = temp_data.loc[i, 'BTC_SMA']
            btc_lma = temp_data.loc[i, 'BTC_LMA']

            # Trading logic for gold using golden cross
            if gold_sma > gold_lma and temp_data.loc[i - 1, 'Gold_SMA'] <= temp_data.loc[i - 1, 'Gold_LMA']:
                # Golden cross: Buy Gold
                if cash > 0:
                    gold += (cash * 0.99) / current_gold_price  # 1% commission
                    cash = 0
            elif gold_sma < gold_lma and temp_data.loc[i - 1, 'Gold_SMA'] >= temp_data.loc[i - 1, 'Gold_LMA']:
                # Death cross: Sell Gold
                if gold > 0:
                    cash += gold * current_gold_price * 0.99  # 1% commission
                    gold = 0

            # Trading logic for BTC using golden cross
            if btc_sma > btc_lma and temp_data.loc[i - 1, 'BTC_SMA'] <= temp_data.loc[i - 1, 'BTC_LMA']:
                # Golden cross: Buy Bitcoin
                if cash > 0:
                    btc += (cash * 0.98) / current_btc_price  # 2% commission
                    cash = 0
            elif btc_sma < btc_lma and temp_data.loc[i - 1, 'BTC_SMA'] >= temp_data.loc[i - 1, 'BTC_LMA']:
                # Death cross: Sell Bitcoin
                if btc > 0:
                    cash += btc * current_btc_price * 0.98  # 2% commission
                    btc = 0

        # Calculate final portfolio value
        final_value = (
            cash
            + (gold * temp_data.iloc[-1]['Gold_Price'])
            + (btc * temp_data.iloc[-1]['BTC_Price'])
        )
        results.append((sma, lma, final_value))

# Convert results to a DataFrame for easier analysis
results_df = pd.DataFrame(results, columns=['SMA', 'LMA', 'Final_Portfolio_Value'])

# Find the row with the maximum final portfolio value
best_result = results_df.loc[results_df['Final_Portfolio_Value'].idxmax()]

# Print the best SMA, LMA, and portfolio value
print(f"Best SMA: {best_result['SMA']}")
print(f"Best LMA: {best_result['LMA']}")
print(f"Best Final Portfolio Value: ${best_result['Final_Portfolio_Value']:.2f}")