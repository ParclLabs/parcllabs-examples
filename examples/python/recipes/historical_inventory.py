"""
To get started with the Parcl Labs API, please follow the quick start
guide to get your API key: 

https://docs.parcllabs.com/docs/quickstart
"""

import os
import requests
import pandas as pd
import matplotlib.pyplot as plt

PARCL_LABS_API_KEY = os.getenv('parcl_labs_api_key') 
PARCL_ID = 5377230 # vegas market

# pass in parcl_id into the url structure, replace with prod URL
url = f'https://api.realestate.parcllabs.com/v1/inventory/{PARCL_ID}/history'

# authorize
header = {
    'Authorization': PARCL_LABS_API_KEY
}

response = requests.get(
    url,
    headers=header
)

# convert the pricefeed key into a pandas dataframe
inventory = pd.DataFrame(response.json()['historical_inventory'])

# Convert the 'date' column to a datetime object
inventory['date'] = pd.to_datetime(inventory['date'])
inventory = inventory.sort_values(by='date', ascending=True)


# Set the 'date' column as the dataframe's index
inventory.set_index('date', inplace=True)

# Calculate percent change for each unit type
inventory['condo_pct_change_from_2010'] = inventory['condo'].pct_change().fillna(0).add(1).cumprod().sub(1).mul(100)
inventory['sfr_pct_change_from_2010'] = inventory['single_family'].pct_change().fillna(0).add(1).cumprod().sub(1).mul(100)
inventory['townhouse_pct_change_from_2010'] = inventory['townhouse'].pct_change().fillna(0).add(1).cumprod().sub(1).mul(100)
inventory['total_pct_change_from_2010'] = inventory['total_units'].pct_change().fillna(0).add(1).cumprod().sub(1).mul(100)

# Create a time series chart using matplotlib
plt.style.use('seaborn-v0_8-darkgrid')
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(inventory['condo_pct_change_from_2010'], label='Condo')
ax.plot(inventory['sfr_pct_change_from_2010'], label='Single Family')
ax.plot(inventory['townhouse_pct_change_from_2010'], label='Townhouse')
ax.plot(inventory['total_pct_change_from_2010'], label='Total Units')

ax.legend()
ax.set_xlabel('Year')
ax.set_ylabel('Percent Change (%)')
ax.set_title('Las Vegas Inventory Percent Change From 2010')

plt.show()
plt.savefig(f'vegas_inventory.png', dpi=300, bbox_inches='tight', pad_inches=0.25)