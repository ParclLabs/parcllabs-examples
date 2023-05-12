"""
To get started with the Parcl Labs API, please follow the quick start
guide to get your API key: 

https://docs.parcllabs.com/docs/quickstart
"""


import os
import requests
from datetime import datetime

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


api_key = os.environ['parcl_labs_api_key']

headers = {
    "Authorization": api_key
}

# markets endpoint will provide all <parcls> available in the API currently
markets_endpoint = "https://api.realestate.parcllabs.com/v1/place/markets"

response = requests.get(markets_endpoint, headers=headers)

markets_json = response.json()


# select some interesting markets
pids = [
    5384169, # Atlanta
    5407714, # Boston
    5822447, # Brooklyn County
    5387853, # Chicago
    5306725, # Denver
    5377230, # Las Vegas
    5373892, # Los Angeles
    5352987, # Miami
    5353022, # Miami Beach
    5372594, # New York
    5378051, # Philly
    5386820, # Phoenix
    5408016, # Portland
    5374321, # San Fran
    5384705, # Seattle
    5503877, # Washington, DC
    5386838, # Scottsdale,
    2900332, # san diego
    2900398, # steamboat springs
    2900229, # palm bay FL
    2899841, # Charlotte
    2900174, # Nashville
    5306666, # CO Springs
    5290547, # Raleigh
    5333209, # Milwaukee
    5332726, # cinci
    5332800, # cleveland
    5328454, # new orleans
    5377717, # pittsburgh
    5307837, # jersey city
    5308252, # Lousiveille
]

# define data structure for custom collection of data elements
data = {}

for pid in pids:
    for v in markets_json:
        if v['parcl_id'] == pid:
            data[pid] = {'name': v['name'].replace('City', ''), 'state': v['state']}


# set start and end times for price feed with today being the max date
end = datetime.today().date()
dte_format = '%m/%d/%Y'
end_format = end.strftime(dte_format)

params = {
    'start': '1/1/2020',
    'end': end_format
}

# grab the price feed and calculate percent change since t0
dt = []
for parcl_id in data.keys():
    price_feed_endpoint = f"https://api.realestate.parcllabs.com/v1/price_feed/{parcl_id}/history"    
    response = requests.get(price_feed_endpoint, params=params, headers=headers).json()
    price_feed = pd.DataFrame(response['price_feed'])
    price_feed = price_feed[['date', 'price']]
    price_feed.index = pd.DatetimeIndex(price_feed['date'])
    price_feed = price_feed.drop('date', axis=1)
    price_feed = price_feed.rename(columns={'price': data[parcl_id]['name']})
    dt.append(price_feed)
    
# concatenate all price feeds into one data structure
res = pd.concat(dt, axis=1)


# Chart Heatmap of Correlation Coefficients
plt.figure(
    figsize=(30, 15)
)

heatmap = sns.heatmap(
    res.corr(), 
    vmin=-1, 
    vmax=1, 
    annot=True
)

heatmap.set_title(
    f'Correlation Heatmap of Home Prices since 1/2020 (data as of {end_format})', 
    fontdict={
        'fontsize':12
    }, 
    pad=12
)