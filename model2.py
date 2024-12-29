import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


# import the data files
gold_data = pd.read_csv('LBMA-GOLD.csv')
btc_data = pd.read_csv('BCHAIN-MKPRU.csv')

# change the date formats for both data sets
gold_data['Date'] = pd.to_datetime(gold_data['Date'], format='%m/%d/%y')
btc_data['Date'] = pd.to_datetime(btc_data['Date'], format='%m/%d/%y')

# align data and merge the data files
gold_data.rename(columns={'USD (PM)': 'Gold_Price'}, inplace=True)
btc_data.rename(columns={'Value': 'BTC_Price'}, inplace=True)
data = pd.merge(gold_data, btc_data, on = 'Date', how = 'outer').sort_values(by = 'Date').ffill()




# Add returns columns for analysis
data['BTC_Returns'] = data['BTC_Price'].pct_change()
data['Gold_Returns'] = data['Gold_Price'].pct_change()
data = data.dropna()  # Remove rows with NaN values caused by pct_change

data['BTC_Trend'] = data['BTC_Returns'].shift(-1)  # Predict next day's BTC trend
data = data.dropna()

features = data[['BTC_Price', 'Gold_Price', 'BTC_Returns']]
target = (data['BTC_Trend'] > 0).astype(int)  # 1 if BTC expected to rise, 0 otherwise

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Train the model
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Initialize variables for the backtest
initial_cash = 1000
btc_position = 0
gold_position = 0
cash = initial_cash
btc_commission = 0.02
gold_commission = 0.01

# Backtesting the strategy
for i in range(len(data) - 1):
    current_btc_price = data.iloc[i]['BTC_Price']
    current_gold_price = data.iloc[i]['Gold_Price']

    # Features for prediction
    current_features = scaler.transform(features.iloc[i:i+1])

    prediction = model.predict(current_features)[0]

    if prediction > 0:  # BTC expected to rise
        if btc_position == 0:  # Buy BTC if we don’t already hold it
            if gold_position > 0:  # Sell Gold if we hold it
                cash = gold_position * current_gold_price * (1 - gold_commission)
                gold_position = 0
            btc_position = (cash * (1 - btc_commission)) / current_btc_price
            cash = 0
    else:  # BTC expected to fall
        if btc_position > 0:  # Sell BTC if we hold it
            cash = btc_position * current_btc_price * (1 - btc_commission)
            btc_position = 0
            gold_position = (cash * (1 - gold_commission)) / current_gold_price
            cash = 0

# Calculate final portfolio value
final_value = (
    cash
    + btc_position * data.iloc[-1]['BTC_Price']
    + gold_position * data.iloc[-1]['Gold_Price']
)

print(f"Final portfolio value: ${final_value:.2f}")
