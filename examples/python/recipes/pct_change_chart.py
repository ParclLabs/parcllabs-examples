import os
import requests
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.express as px


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
for parcl_id in data.keys():
    price_feed_endpoint = f"https://api.realestate.parcllabs.com/v1/price_feed/{parcl_id}/history"    
    response = requests.get(price_feed_endpoint, params=params, headers=headers).json()
    price_feed = pd.DataFrame(response['price_feed'])
    price_feed['pct_change_since_start'] = (1-price_feed.iloc[0].price / price_feed.price)
    price_feed['name'] = data[parcl_id]['name']
    data[parcl_id]['price_feed'] = price_feed

# concatenate all price feeds into one data structure
out = pd.concat([data[parcl_id]['price_feed'] for parcl_id in data.keys()])
# fmt date
out['date'] = pd.to_datetime(out['date'])

# plot
out = out.rename(columns={'name': "Market"})
fig1 = px.line(
    out, x='date', 
    y='pct_change_since_start', 
    color='Market', 
    render_mode='webgl', 
    labels={
    'pct_change_since_start': "Percent Change (Price per Square Foot)",
    },
    title='Housing Prices: Percent Change in Price per Square Foot Since 1/2020',
    color_discrete_sequence=px.colors.qualitative.Dark24
)

fig1.update_layout(
    autosize=False,
    width=1250,
    height=700,
    title_x=0.5,
    xaxis_title=None
)

fig1.update_xaxes(tickangle=45)

fig1.update_yaxes(tickformat='.0%')