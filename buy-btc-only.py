from organize_data import *

# Initial investment
initial_cash = 1000  # Starting capital in USD

# Prices on the first and last day
btc_start_price = data.iloc[0]['BTC_Price']
btc_end_price = data.iloc[-1]['BTC_Price']

# Number of BTC bought on day 1
btc_position = initial_cash / btc_start_price

# Final portfolio value
final_value = btc_position * btc_end_price

print(f"Final portfolio value with buy-and-hold strategy: ${final_value:.2f}")