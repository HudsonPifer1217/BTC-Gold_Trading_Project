from organize_data import *
from testing_LMA_and_SMA import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

##convert results to a 3D plot
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
ax.set_title('Final Portfolio Value vs SMA vs LMA for Gold and BTC')

plt.show()


#Analyze the result to find the best combination of SMA and LMA
results_df = pd.DataFrame(results, columns=['SMA', 'LMA', 'Final_Portfolio_Value'])

best_combination = results_df.loc[results_df['Final_Portfolio_Value'].idxmax()]


## HEATMAP

# Keep the row with the highest Final_Portfolio_Value for each (SMA, LMA) combination
results_df = results_df.groupby(['SMA', 'LMA'], as_index=False)['Final_Portfolio_Value'].max()

# Check for duplicates
#print("Remaining duplicates:", results_df.duplicated(subset=['SMA', 'LMA']).sum())

# Create the heatmap
heatmap_data = results_df.pivot(index='LMA', columns='SMA', values='Final_Portfolio_Value')

# Plot heatmap
plt.figure(figsize=(12, 8))
plt.title('Portfolio Value Heatmap (SMA vs LMA) for Gold and BTC', fontsize=16)
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



