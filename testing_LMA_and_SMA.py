import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from organize_data import *

# define ranges for SMA and LMA
sma_values= range(5,51, 2)  ##SMA from 5 to 50 days, going 2 days at a time
lma_values = range(30, 200, 10) ##LMA from 30 to 150 days, going 10 days at a time

results = []

for sma in sma_values:
    for lma in lma_values:
        if sma >= lma:  #skip over invalid SMA and LMA combinations
            continue
        #calculate moving avgs:
        data['Gold_SMA'] = data['Gold_Price'].rolling(window=sma).mean()
        data['Gold_LMA'] = data['Gold_Price'].rolling(window=lma).mean()
        data['BTC_SMA'] = data['BTC_Price'].rolling(window=sma).mean()
        data['BTC_LMA'] = data['BTC_Price'].rolling(window=lma).mean()

        #drop empty days and reset portfolio:
        temp_data = data.dropna().reset_index(drop=True)
        cash, gold, btc = 1000, 0, 0

        #Stimulate trading for given SMA/ LMA combination:
        for i in range(len(temp_data)-1):
            current_gold_price = temp_data.loc[i, 'Gold_Price']
            current_btc_price = temp_data.loc[i, 'BTC_Price']
            gold_sma = temp_data.loc[i, 'Gold_SMA']
            gold_lma = temp_data.loc[i, 'Gold_LMA']
            btc_sma = temp_data.loc[i, 'BTC_SMA']
            btc_lma = temp_data.loc[i, 'BTC_LMA']

            ## TRADING USING GOLDEN AND DEATH CROSSES

            #trading logic for gold:
            if gold_sma > gold_lma:    #Buy Gold
                if cash > 0:   ## if there is cash...
                    gold += (cash * 0.99)/ current_gold_price   # 1% commission
                    cash = 0    ## go all in
            elif gold_sma < gold_lma and gold > 0:   # Sell Gold
                cash += gold * current_gold_price * 0.99    # 1% commission
                gold = 0  #sell all the gold

            #trading logic for BTC:
            if btc_sma > btc_lma:  # Buy Bitcoin
                if cash > 0:
                    btc += (cash * 0.98) / current_btc_price  # 2% commission
                    cash = 0
            elif btc_sma < btc_lma and btc > 0:  # Sell Bitcoin
                cash += btc * current_btc_price * 0.98  # 2% commission
                btc = 0

            final_value = cash + (gold * temp_data.iloc[-1]['Gold_Price']) + (btc * temp_data.iloc[-1]['BTC_Price'])
            results.append((sma, lma, final_value))





