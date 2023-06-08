"""
To get started with the Parcl Labs API, please follow the quick start
guide to get your API key: 

https://docs.parcllabs.com/docs/quickstart
"""

import os
import requests

import pandas as pd
import plotly.express as px


# get your api key
# see: https://docs.parcllabs.com/docs/quickstart
api_key = os.environ['parcl_labs_api_key']

headers = {
    "Authorization": api_key
}

#### GET MARKETS ####
# get market details
markets_endpoint = "https://api.realestate.parcllabs.com/v1/place/markets"

response = requests.get(markets_endpoint, headers=headers)

markets_json = response.json()

# filtering analysis to cs markets

cs_markets = [
    2900336, # San Fran
    2900078, # Los Angeles
    2900187, # New York
    2900245, # Phoenix
    2900332, # San Diego
    2900353, # Seattle
    2899845, # Chicago
    2900128, # Miami
    2899625, # Boston
    2899750, # Denver
    2887280, # Atlanta
    2900049, # Las Vegas
    2900475, # DC
    2900417, # Tampa
    2900266, # Portland
    2900137, # Minneapolis
    2899841, # Charlotte
    2899753, # Detroit
    2899654 # Cleveland
]

#### GET DATA ####
# get financials, and last price for markets
# unpack market names, standard deviation of returns, cagr

def get_market(
    markets_json,
    parcl_id
):
    for m in markets_json:
        if parcl_id == m['parcl_id']:
            return m

names = []
cagrs = []
vols = []
states = []
last_prices = []
location_types = []

for parcl_id in cs_markets:
    
    # Get market characteristics
    market = get_market(markets_json, parcl_id)
    location_type = market['location_type']
    name = market['name']
    state = market['state']
    
    
    financials_endpoint = f"https://api.realestate.parcllabs.com/v1/financials/{parcl_id}/current"
    last_price_endpoint = 'https://api.realestate.parcllabs.com/v1/price_feed/latest'
    
    last_price_params = {
        'parcl_id': parcl_id
    }
    
    financials = requests.get(financials_endpoint, headers=headers).json()
    last_price = requests.get(last_price_endpoint, headers=headers, params=last_price_params).json()
    
    cagr = financials['cagr']
    annual_vol = financials['annual_volatitily']
    last_price = last_price['price_feeds'][str(parcl_id)]['price']
    names.append(f"{name.split('-')[0]}") # clean up msa names
    cagrs.append(cagr)
    vols.append(annual_vol)
    states.append(state)
    last_prices.append(last_price)
    location_types.append(location_type)
    
# create dataframe for charting
chartdf = pd.DataFrame({
    'name': names,
    'state': states,
    'cagr': cagrs,
    'vol': vols,
    'price': last_prices
})

#### Chart Risk vs. Return ####
fig = px.scatter(
    chartdf, 
    x="vol", 
    y="cagr", 
    color="state",        
    size='price',
    hover_data=['name'],
    text='name',
    labels={
        'vol': "Annualized Volatility",
        'cagr': '1-Year Annualized Return'
    },
    title='Case Shiller Metros - Risk vs. Return by Housing Market'
)

fig.update_layout(
    autosize=False,
    width=1000,
    height=700,
    title_x=0.5,
    yaxis={'tickformat': ',.0%'},
    xaxis={'tickformat': ',.0%'}
)


fig.show()