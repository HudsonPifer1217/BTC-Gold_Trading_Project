import pandas as pd
import numpy as np


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





