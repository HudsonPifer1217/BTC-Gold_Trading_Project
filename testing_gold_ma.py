from organize_data import *
import matplotlib.pyplot as plt

results = []
# define ranges for SMA and LMA
sma_values= range(1,51, 2)  ##SMA from 5 to 50 days, going 2 days at a time
lma_values = range(30, 200, 10) ##LMA from 30 to 150 days, going 10 days at a time

for sma in sma_values:
    for lma in lma_values:
        if sma >= lma:  #skip over invalid SMA and LMA combinations
            continue
        #calculate moving avgs:
        data['Gold_SMA'] = data['Gold_Price'].rolling(window=sma).mean()
        data['Gold_LMA'] = data['Gold_Price'].rolling(window=lma).mean()

        #drop empty days and reset portfolio:
        temp_data = data.dropna().reset_index(drop=True)
        cash, gold, btc = 1000, 0, 0

        #Stimulate trading for given SMA/ LMA combination:
        for i in range(len(temp_data)-1):
            current_gold_price = temp_data.loc[i, 'Gold_Price']
            gold_sma = temp_data.loc[i, 'Gold_SMA']
            gold_lma = temp_data.loc[i, 'Gold_LMA']

            ## TRADING USING GOLDEN AND DEATH CROSSES

            # trading logic for gold:
            if gold_sma > gold_lma:  # Buy Gold
                if cash > 0:  ## if there is cash...
                    gold += (cash * 0.99) / current_gold_price  # 1% commission
                    cash = 0  ## go all in
            elif gold_sma < gold_lma and gold > 0:  # Sell Gold
                cash += gold * current_gold_price * 0.99  # 1% commission
                gold = 0  # sell all the gold

            final_value = cash + (gold * temp_data.iloc[-1]['Gold_Price']) + (btc * temp_data.iloc[-1]['BTC_Price'])
            results.append((sma, lma, final_value))


sma_vals, lma_vals, final_vals = zip(*results)
sma_vals = list(sma_vals)
lma_vals = list(lma_vals)
final_vals = list(final_vals)

# create the 3D plot
fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot
ax.scatter(sma_vals, lma_vals, final_vals, c=final_vals, cmap = 'viridis', marker='o')

ax.set_xlabel('Short Moving Average SMA')
ax.set_ylabel('Long Moving Average LMA')
ax.set_zlabel('Final Portfolio Value')
ax.set_title('Final Portfolio Value vs SMA vs LMA for Gold')

plt.show()


#Analyze the result to find the best combination of SMA and LMA
results_df = pd.DataFrame(results, columns=['SMA', 'LMA', 'Final_Portfolio_Value'])
results_df = results_df.drop_duplicates()

best_combination = results_df.loc[results_df['Final_Portfolio_Value'].idxmax()]
print(len(results_df))
print(best_combination)
print(results_df[(results_df['Final_Portfolio_Value'] > 1500)])

'''
Results: 
SMA                         1.000000
LMA                        60.000000
Final_Portfolio_Value    1510.952928
'''
## HEATMAP

# Keep the row with the highest Final_Portfolio_Value for each (SMA, LMA) combination
results_df = results_df.groupby(['SMA', 'LMA'], as_index=False)['Final_Portfolio_Value'].max()

# Check for duplicates
print("Remaining duplicates:", results_df.duplicated(subset=['SMA', 'LMA']).sum())

# Create the heatmap
heatmap_data = results_df.pivot(index='LMA', columns='SMA', values='Final_Portfolio_Value')

# Plot heatmap
plt.figure(figsize=(12, 8))
plt.title('Portfolio Value Heatmap (SMA vs LMA) for Gold', fontsize=16)
heatmap = plt.imshow(heatmap_data, cmap='viridis', aspect='auto', origin='lower')
plt.colorbar(heatmap, label='Final Portfolio Value')

# Add axis labels
plt.xlabel('Short Moving Average (SMA)', fontsize=14)
plt.ylabel('Long Moving Average (LMA)', fontsize=14)

# Add tick labels for SMA and LMA
plt.xticks(range(len(heatmap_data.columns)), heatmap_data.columns, rotation=45)
plt.yticks(range(len(heatmap_data.index)), heatmap_data.index)

# Adjust layout
plt.tight_layout()
plt.show()