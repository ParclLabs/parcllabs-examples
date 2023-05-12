"""
To get started with the Parcl Labs API, please follow the quick start
guide to get your API key: 

https://docs.parcllabs.com/docs/quickstart
"""


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


# markets endpoint will provide all <parcls> available in the API currently along with market metadata like name
markets_endpoint = f"https://api.realestate.parcllabs.com/v1/place/markets"

response = requests.get(markets_endpoint, headers=headers)

markets_json = response.json()


# create data structure for data manipulations and metadata
pids = [
    5332726, # cinci
    5332800, # cleveland
    5328454, # new orleans
    5377717, # pittsburgh
    5307837, # jersey city
    5308252, # Lousiveille
    5353022, # Miami Beach
]
# define data structure for custom collection of data elements
data = {}

for pid in pids:
    for v in markets_json:
        if v['parcl_id'] == pid:
            data[pid] = {'name': v['name'].replace('City', ''), 'state': v['state']}


# financial history endpoint will provide historical financial metrics for
# given parcl_id
vols = []

for pid in data.keys():
    financial_historical_endpoint = f"https://api.realestate.parcllabs.com/v1/financials/{pid}/history"

    response = requests.get(financial_historical_endpoint, headers=headers)

    finanical_json = response.json()
    vol = pd.DataFrame(finanical_json['metrics']).sort_values('date')
    vol['pct_change'] = (1-vol.iloc[0].annual_volatility / vol.annual_volatility)
    vol['Market'] = data[pid]['name']
    data[pid]['vols'] = vol
    vols.append(vol)


# create one data structure
df = pd.concat(vols)


# Create volatility chart
df['date'] = pd.to_datetime(df['date'])

fig1 = px.line(
    df, x='date', 
    y='annual_volatility', 
    color='Market', 
    render_mode='webgl', 
    labels={
    'annual_volatility': "Annual Volatility",
    },
    title='Annual Volatility by Housing Market',
    color_discrete_sequence=px.colors.qualitative.Dark24
)

fig1.update_layout(
    autosize=False,
    width=500,
    height=500,
    title_x=0.5,
    xaxis_title=None
)

fig1.update_xaxes(tickangle=45)
fig1.update_yaxes(tickformat='.0%')