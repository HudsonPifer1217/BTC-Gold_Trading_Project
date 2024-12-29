from organize_data import *



def calculate_final_value(data):
    # Include all the logic to calculate the final portfolio value
    cash, btc = 1000, 0
    sma, lma = 45, 120
    data['BTC_SMA'] = data['BTC_Price'].rolling(window=sma).mean()
    data['BTC_LMA'] = data['BTC_Price'].rolling(window=lma).mean()
    temp_data = data.dropna().reset_index(drop=True)

    for i in range(len(temp_data)):
        current_btc_price = temp_data.loc[i, 'BTC_Price']
        btc_sma = temp_data.loc[i, 'BTC_SMA']
        btc_lma = temp_data.loc[i, 'BTC_LMA']

        if btc_sma > btc_lma and cash > 0:
            btc += (cash * 0.98) / current_btc_price  # 2% commission
            cash = 0
        elif btc_sma < btc_lma and btc > 0:
            cash += btc * current_btc_price * 0.98  # 2% commission
            btc = 0

    final_value = cash + btc * temp_data.loc[len(temp_data) - 1, 'BTC_Price']
    return final_value
