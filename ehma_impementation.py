from organize_data import *
from ehma_funcs import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# Define periods for testing EHMA
btc_period = 20  # Adjust this to optimize for Bitcoin
gold_period = 50  # Adjust this to optimize for gold

# Run EHMA-based strategy
final_portfolio_value = integrate_ehma_with_rsi(data, btc_period, gold_period)

# Print the result
print(f"Final Portfolio Value with EHMA Strategy: ${final_portfolio_value:.2f}")


best_value = 0
best_btc_period = 0
best_gold_period = 0

# Test a range of periods
for btc_period in range(5, 51, 5):  # Bitcoin EHMA periods
    for gold_period in range(10, 101, 10):  # Gold EHMA periods
        portfolio_value = integrate_ehma_with_rsi(data, btc_period, gold_period)
        if portfolio_value > best_value:
            best_value = portfolio_value
            best_btc_period = btc_period
            best_gold_period = gold_period

# Print the best results
print(f"Best BTC EHMA Period: {best_btc_period}")
print(f"Best Gold EHMA Period: {best_gold_period}")
print(f"Best Portfolio Value: ${best_value:.2f}")



# Calculate EHMA for a specific period
data['BTC_EHMA'] = calculate_ehma(data['BTC_Price'], 20)
data['Gold_EHMA'] = calculate_ehma(data['Gold_Price'], 50)

# Plot Bitcoin prices with EHMA
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['BTC_Price'], label='Bitcoin Price', color='blue')
plt.plot(data['Date'], data['BTC_EHMA'], label='Bitcoin EHMA (20)', color='orange')
plt.title('Bitcoin Price vs. EHMA')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.show()

# Plot Gold prices with EHMA
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['Gold_Price'], label='Gold Price', color='green')
plt.plot(data['Date'], data['Gold_EHMA'], label='Gold EHMA (50)', color='red')
plt.title('Gold Price vs. EHMA')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.show()


