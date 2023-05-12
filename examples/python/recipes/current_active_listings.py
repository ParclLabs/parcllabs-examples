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

# authorize
headers = {
    'Authorization': PARCL_LABS_API_KEY
}

nyc_markets = [
    5372594, # new york city
    5822447, # brooklyn
    5822484 # manhattan
]

markets_endpoint = "https://api.realestate.parcllabs.com/v1/place/markets"

response = requests.get(markets_endpoint, headers=headers)

markets_json = response.json()

#### GET DATA ####
# unpack market names

def get_market(
    markets_json,
    parcl_id
):
    for m in markets_json:
        if parcl_id == m['parcl_id']:
            return m

names = []
listings = []
location_types = []

for parcl_id in nyc_markets:
    
    # Get market characteristics
    market = get_market(markets_json, parcl_id)
    location_type = market['location_type']
    name = market['name']    
    
    listings_endpoint = f'https://api.realestate.dev.parcllabs.com/v1/listings/{parcl_id}/current'

    listings_response = requests.get(listings_endpoint, headers=headers).json()
    
    listing = listings_response['listings']['listings_30_day']
    date = listings_response['listings']['date']

    names.append(name)
    listings.append(listing)
    location_types.append(location_type)
    
# create dataframe
listings_df = pd.DataFrame({
    'name': names,
    'listings_30_day': listings,
    'location_type': location_types
})

# Extract the data for the donut chart
ny_total = listings_df[listings_df['name'] == 'New York']['listings_30_day'].iloc[0]
brooklyn = listings_df[listings_df['name'] == 'Brooklyn County']['listings_30_day'].iloc[0]
manhattan = listings_df[listings_df['name'] == 'Manhattan County']['listings_30_day'].iloc[0]
other = ny_total - brooklyn - manhattan

plt.style.use('seaborn-v0_8-pastel')

# Create the figure and axes
fig, ax = plt.subplots()

# Create the pie chart
wedges, texts, autotexts = ax.pie([brooklyn, manhattan, other], 
                                  radius=1.2, 
                                  wedgeprops={'width': 0.4, 'edgecolor': 'w'},
                                   labels=[f'Brooklyn\n{brooklyn:,}', f'Manhattan\n{manhattan:,}', f'Other Boroughs\n{other:,}'],
                                  autopct='%1.1f%%',
                                  pctdistance=0.8)

# Create a white circle to make a donut chart
circle = plt.Circle((0,0), 0.8, color='white')
ax.add_artist(circle)

# Add the total number of listings in the center of the donut
ax.text(0, 0, f'Total Listings:\n{ny_total:,}', 
        ha='center', 
        va='center')

# Set the title
ax.set_title('On Market Listings in the Past Month: NYC')

# Show the chart
plt.show()