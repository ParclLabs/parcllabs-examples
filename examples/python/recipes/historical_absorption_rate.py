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
    5380879, # Austin
    5381001, # Dallas
    5381035 #Hosuton
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
absorption = []
dates = []

for parcl_id in markets:
    
    # Get market characteristics
    market = get_market(markets_json, parcl_id)
    name = market['name']    
    
    abs_endpoint = f'https://api.realestate.parcllabs.com/v1/absorption/{parcl_id}/history'

    abs_response = requests.get(abs_endpoint, headers=headers).json()

    for item in abs_response['historical_absorption_rate']:
        ar = item['absorption_rate']
        date = item['date']

        names.append(name)
        absorption.append(ar)
        dates.append(date)

# create dataframe
ar_df = pd.DataFrame({
    'name': names,
    'absorption_rate': absorption,
    'date': dates
})

# Convert the 'date' column to a datetime object
ar_df['date'] = pd.to_datetime(ar_df['date'])
ar_df = ar_df.sort_values(by='date', ascending=True)

# Create a time series chart using matplotlib
plt.style.use('seaborn-v0_8-darkgrid')
fig, ax = plt.subplots(figsize=(10, 6))

cities = sorted(ar_df['name'].unique())

for c in cities:
    ax.plot(ar_df[(ar_df['name'] == c)]['date'],
            ar_df[(ar_df['name'] == c)]['absorption_rate'],
            label = c)

#format the visualization
ax.legend()
ax.set_xlabel('Date')
ax.set_ylabel('Absorption Rate')
ax.set_title('Daily Absorption Rate: PHX, SF and CHI')

plt.show()