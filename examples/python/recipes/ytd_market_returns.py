"""
To get started with the Parcl Labs API, please follow the quick start
guide to get your API key: 

https://docs.parcllabs.com/docs/quickstart
"""

import os
import requests
from datetime import datetime

import pandas as pd
import plotly.express as px


api_key = os.environ['parcl_labs_api_key']

headers = {
    "Authorization": api_key
}

params = {
    'location_type': 'MSA'
}


# markets endpoint will provide all <parcls> available in the API currently
markets_endpoint = "https://api.realestate.parcllabs.com/v1/place/markets"

response = requests.get(markets_endpoint, headers=headers, params=params)

markets_json = response.json()

# get relevant data from api
# set start and end times for price feed with today being the max date
end = datetime.today().date()
dte_format = '%m/%d/%Y'
end_format = end.strftime(dte_format)

params = {
    'start': '1/1/2023',
    'end': end_format
}

alldata = []

# grab the price feed and calculate percent change since t0
for market in markets_json:

    parcl_id = market['parcl_id']
    
    price_feed_endpoint = f"https://api.realestate.parcllabs.com/v1/price_feed/{parcl_id}/history" 
    
    response = requests.get(
        price_feed_endpoint, 
        params=params, 
        headers=headers
    ).json()
    
    
    # demographics for popuplation
    demo = f"https://api.realestate.parcllabs.com/v1/place/{parcl_id}/demographics"

    demographics_params = {
        'category': 'population'
    }

    d = requests.get(
        demo, 
        headers=headers, 
        params=demographics_params
    )
    
    ddf = pd.DataFrame(d.json()['population'])
    
    pid_total_pop = ddf.loc[(ddf['year'] == 2021) & (ddf['variable']=='pop_total')]['value'].values[0]
    
    price_feed = pd.DataFrame(response['price_feed'])
    price_feed['pct_change_since_start'] = (1-price_feed.iloc[0].price / price_feed.price)
    price_feed['name'] = market['name']
    record = pd.DataFrame({
        'name': market['name'],
        'pct_change': price_feed.iloc[-1].pct_change_since_start,
        'last_price': price_feed.iloc[-1].price,
        'region': market['census_region'],
        'population': pid_total_pop
    }, index=[0])
    alldata.append(record)


# get top 5 most populous areas by region
df = pd.concat(alldata)
df = df.sort_values(['region', 'population'], ascending=False)
df = df.groupby('region').head(8).reset_index(drop=True)
df = df.sort_values(['region', 'pct_change'], ascending=False)

# plot
fig = px.scatter(
    df,
    x='name',
    y='pct_change',
    size='last_price',
    color='region',
    color_discrete_sequence=px.colors.qualitative.Plotly
)

fig.update_traces(marker=dict(
        line=dict(
        width=0.5,
        color='DarkSlateGrey')
    ))
fig.update_layout(margin=dict(l=20, r=20),
                  title=f'Real Estate Market Returns - YTD',
                  title_font=dict(size = 20),
                  autosize=True,
                 height=800,
                 xaxis_title=None,
                 yaxis_title='Percent Returns',
                  title_x=0.5,
                 )

fig.update_yaxes(tickformat='.0%')