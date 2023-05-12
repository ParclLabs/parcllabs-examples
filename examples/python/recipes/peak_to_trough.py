"""
Example of how to pull down a pricefeed, 
and run a simple peak to trough analysis
to understand which markets are in correction
territory. 
"""

import os
import requests
from datetime import datetime

import pandas as pd


PARCL_LABS_API_KEY = os.getenv('parcl_labs_api_key')

START = '1/1/2022'
END = datetime.now().strftime('%m/%d/%Y')

markets = {
    2900078: 'Los Angeles',
    2900187: 'New York',
    2900245: 'Phoenix',
    2899845: 'Chicago',
    2899625: 'Boston',
    2899750: 'Denver',
    2887280: 'Atlanta',
    2900049: 'Las Vegas',
    2900475: 'Washington, DC',
    2900417: 'Tampa',
    2900266: 'Portland',
    2900137: 'Minneapolis',
    2899841: 'Charlotte',
    2899753: 'Detroit',
    2899654: 'Cleveland',
    2900336: 'San Francisco',
    2900332: 'San Diego',
    2900353: 'Seattle',
}

results = []

for parcl_id, mkt_name in markets.items():

    # pass in parcl_id into the url structure
    url = f'https://api.realestate.parcllabs.com/v1/price_feed/{parcl_id}/history'

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
    pricefeed['date'] = pd.to_datetime(pricefeed['date'])
    pricefeed = pricefeed.sort_values('date')
    peak_2022 = pricefeed.loc[pricefeed['date']< datetime.strptime('1/1/2023', '%m/%d/%Y')]['parcl_price_feed'].max()
    last_price = pricefeed['parcl_price_feed'].values[-1]
    peak_to_trough = (last_price-peak_2022)/peak_2022
    results.append((mkt_name, peak_to_trough))
    
correction_territory_threshold = -.1

results = sorted(results, key=lambda x: x[1])
for r in results:
    correction_territory = 'Correction Territory' if r[1] < correction_territory_threshold else 'Not in Correction Territory'
    print(f"Peak to current {r[0]}: {r[1]:.2%} -- {correction_territory}")