"""
Example of how to pull down a pricefeed, 
and create a pandas dataframe for subsequent
analysis or plotting
"""

import os
import requests

import pandas as pd


PARCL_LABS_API_KEY = os.getenv('api_key')

START = '1/1/2022'
END = '1/1/2023'
PARCL_ID = 2900187 # cleveland market

# pass in parcl_id into the url structure
url = f'https://api.realestate.parcllabs.com/v1/price_feed/{PARCL_ID}/history'

# define required parameters - specs: 
# https://docs.parcllabs.com/reference/get_place-parcl-id-price-feed
params = {
    'start': START,
    'end': END
}
# authorize
header = {
    'Authorization': PARCL_LABS_API_KEY
}

response = requests.get(
    url,
    headers=header,
    params=params
)

# convert the pricefeed key into a pandas dataframe
pricefeed = pd.DataFrame(response.json()['pricefeed'])
print(pricefeed.head())

#          date  parcl_price_feed
# 0  2022-01-01            349.58
# 1  2022-01-02            349.07
# 2  2022-01-03            349.18
# 3  2022-01-04            349.27
# 4  2022-01-05            349.43