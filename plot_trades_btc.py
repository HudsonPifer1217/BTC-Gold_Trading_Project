from organize_data import *
from testing_btc_ma import *
import matplotlib.pyplot as plt

from best_btc_outcome import calculate_final_value

# Call the function to get the final value
final_portfolio_value = calculate_final_value(data)
print(f"Final Portfolio Value from Imported Logic: ${final_portfolio_value:.2f}")


# Define Optimal SMA and LMA
sma = 45
lma = 120

# Initialize portfolio and signal lists



data['BTC_SMA'] = data['BTC_Price'].rolling(window=sma).mean()
data['BTC_LMA'] = data['BTC_Price'].rolling(window=lma).mean()

#drop empty days and reset portfolio:
temp_data = data.dropna().reset_index(drop=True)
cash, btc, gold = 1000, 0, 0
buy_signals = []
sell_signals = []
portfolio_values = []
#Stimulate trading for given SMA/ LMA combination:
for i in range(len(temp_data)):
    current_btc_price = temp_data.loc[i, 'BTC_Price']

    btc_sma = temp_data.loc[i, 'BTC_SMA']
    btc_lma = temp_data.loc[i, 'BTC_LMA']

    ## TRADING USING GOLDEN AND DEATH CROSSES

    #trading logic for BTC:
    if btc_sma > btc_lma:  # Buy Bitcoin
        if cash > 0:
            btc += (cash * 0.98) / current_btc_price  # 2% commission
            cash = 0
            buy_signals.append((temp_data.loc[i, 'Date'], current_btc_price))
    elif btc_sma < btc_lma and btc > 0:  # Sell Bitcoin
        cash += btc * current_btc_price * 0.98  # 2% commission
        btc = 0
        sell_signals.append((temp_data.loc[i, 'Date'], current_btc_price))

    portfolio_values.append(cash + btc * current_btc_price)
    final_value = cash + (gold * temp_data.iloc[-1]['Gold_Price']) + (btc * temp_data.iloc[-1]['BTC_Price'])

    results.append((sma, lma, final_value))


final_value = cash + (gold * temp_data.loc[len(temp_data) - 1, 'Gold_Price']) + (btc * temp_data.loc[len(temp_data) - 1, 'BTC_Price'])
print(f"Final Portfolio Value: ${final_value:.2f}")

# Extract buy and sell dates and prices
if buy_signals:
    buy_dates, buy_prices = zip(*buy_signals)
else:
    buy_dates, buy_prices = [], []

if sell_signals:
    sell_dates, sell_prices = zip(*sell_signals)
else:
    sell_dates, sell_prices = [], []
# Create a new figure
plt.figure(figsize=(12, 6))

# Plot BTC Price, SMA, and LMA
plt.plot(temp_data['Date'], temp_data['BTC_Price'], label='BTC Price', color='blue', zorder=1)
plt.plot(temp_data['Date'], temp_data['BTC_SMA'], label=f'BTC SMA ({sma})', color='orange', linestyle='--', zorder=1)
plt.plot(temp_data['Date'], temp_data['BTC_LMA'], label=f'BTC LMA ({lma})', color='green', linestyle='--', zorder=1)

# Plot buy and sell signals
plt.scatter(buy_dates, buy_prices, label='Buy', color='green', marker='^', s=100, alpha=1, edgecolors='black', zorder=3)
plt.scatter(sell_dates, sell_prices, label='Sell', color='red', marker='v', s=100, alpha=1, edgecolors='black', zorder=3)

# Plot portfolio value on the same y-axis
plt.plot(temp_data['Date'], portfolio_values, label='Portfolio Value', color='purple', linestyle='-.', zorder=2)

# Add labels, title, and legend
plt.title(f'Trades for BTC with SMA={sma}, LMA={lma}')
plt.xlabel('Date')
plt.ylabel('Value (USD)')
plt.legend()
plt.grid()
plt.tight_layout()

# Show the plot
#plt.show()



