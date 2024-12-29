import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from attempt2.model2 import scaler

# Import the data files (assuming `data` has been preprocessed as earlier)
gold_data = pd.read_csv('LBMA-GOLD.csv')
btc_data = pd.read_csv('BCHAIN-MKPRU.csv')

# Change the date formats for both data sets
gold_data['Date'] = pd.to_datetime(gold_data['Date'], format='%m/%d/%y')
btc_data['Date'] = pd.to_datetime(btc_data['Date'], format='%m/%d/%y')

# Align data and merge the data files
gold_data.rename(columns={'USD (PM)': 'Gold_Price'}, inplace=True)
btc_data.rename(columns={'Value': 'BTC_Price'}, inplace=True)
data = (
    pd.merge(gold_data, btc_data, on='Date', how='outer')
    .sort_values(by='Date')
    .ffill()  # Fill missing values forward
)

# Add returns and lagged features
data['BTC_Returns'] = data['BTC_Price'].pct_change()
data['Gold_Returns'] = data['Gold_Price'].pct_change()
for lag in range(1, 6):  # Adding 5 lagged features
    data[f'BTC_Returns_Lag{lag}'] = data['BTC_Returns'].shift(lag)

# Target: 1 if BTC's next day return is positive, 0 otherwise
data['BTC_Trend'] = (data['BTC_Returns'].shift(-1) > 0).astype(int)

# Adding technical indicators (example: rolling mean/volatility)
data['BTC_RollingMean_7'] = data['BTC_Price'].rolling(7).mean()
data['BTC_RollingStd_7'] = data['BTC_Price'].rolling(7).std()

# Drop rows with NaN values
data = data.dropna()

# Features and target
features = data[['BTC_Price', 'Gold_Price', 'BTC_Returns', 'BTC_RollingMean_7', 'BTC_RollingStd_7'] +
                [f'BTC_Returns_Lag{lag}' for lag in range(1, 6)]]
target = data['BTC_Trend']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Train an improved Random Forest
rf = RandomForestClassifier(n_estimators=300, max_depth=15, random_state=42)
rf.fit(X_train, y_train)

# Evaluate performance
y_pred = rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")



# Initialize trading parameters
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

    # Predict BTC trend
    current_features = scaler.transform(features.iloc[i:i+1])
    prediction = rf.predict(current_features)[0]

    if prediction == 1:  # BTC expected to rise
        if btc_position == 0:  # Buy BTC if not already held
            if gold_position > 0:  # Sell gold if held
                cash = gold_position * current_gold_price * (1 - gold_commission)
                gold_position = 0
            btc_position = (cash * (1 - btc_commission)) / current_btc_price
            cash = 0
    else:  # BTC expected to fall
        if btc_position > 0:  # Sell BTC if held
            cash = btc_position * current_btc_price * (1 - btc_commission)
            btc_position = 0
            gold_position = (cash * (1 - gold_commission)) / current_gold_price
            cash = 0

# Final portfolio value
final_value = (
    cash
    + btc_position * data.iloc[-1]['BTC_Price']
    + gold_position * data.iloc[-1]['Gold_Price']
)
print(f"Final portfolio value: ${final_value:.2f}")
