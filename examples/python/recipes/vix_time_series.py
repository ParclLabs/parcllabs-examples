"""
To get started with the Parcl Labs API, please follow the quick start
guide to get your API key: 

https://docs.parcllabs.com/docs/quickstart
"""

import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

PARCL_LABS_API_KEY = os.getenv('parcl_labs_api_key') 

# authorize
headers = {
    'Authorization': PARCL_LABS_API_KEY
}

markets = [
    5374321, # SF city
    5387853, # Chicago City
    5386820 # PHX City
]

markets_endpoint = "https://api.realestate.parcllabs.com/v1/place/markets"

response = requests.get(markets_endpoint, headers=headers)

markets_json = response.json()

# unpack market names

def get_market(
    markets_json,
    parcl_id
):
    for m in markets_json:
        if parcl_id == m['parcl_id']:
            return m
        
names = []
vix = []
dates = []

for parcl_id in markets:
    
    # Get market characteristics
    market = get_market(markets_json, parcl_id)
    name = market['name']    
    
    vix_endpoint = f'https://api.realestate.parcllabs.com/v1/financials/{parcl_id}/volatility'

    vix_response = requests.get(vix_endpoint, headers=headers).json()
    

    for item in vix_response['volatility']:
        vol = item['volatility']
        date = item['date']

        names.append(name)
        vix.append(vol)
        dates.append(date)
    
# create dataframe
vix_df = pd.DataFrame({
    'name': names,
    'vix': vix,
    'date': dates
})

# Convert the 'date' column to a datetime object
vix_df['date'] = pd.to_datetime(vix_df['date'])
vix_df = vix_df.sort_values(by='date', ascending=True)

# Create a time series chart using matplotlib
plt.style.use('seaborn-v0_8-darkgrid')
fig, ax = plt.subplots(figsize=(10, 6))

cities = sorted(vix_df['name'].unique())

for c in cities:
    ax.plot(vix_df[(vix_df['name'] == c)]['date'],
            vix_df[(vix_df['name'] == c)]['vix'],
            label = c)

#format the visualization
ax.legend()
ax.set_xlabel('Date')
ax.set_ylabel('VIX')
ax.set_title('Daily Market Volatility: PHX, SF and CHI')

#ax.grid(False)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))

plt.show()