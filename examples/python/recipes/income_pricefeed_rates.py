import os
import requests

import pandas as pd


#### AUTH HEADER ####
# create authorization header
PARCL_LABS_API_KEY = os.environ['parcl_labs_api_key']

header = {
    'Authorization': PARCL_LABS_API_KEY
}

##### GET ALL MARKETS AVAILABLE IN API #####
# get all available parcl labs markets in the pilot program
markets = requests.get(
    'https://api.realestate.parcllabs.com/v1/place/markets', 
    headers=header
).json()


# get all msa's
df = pd.DataFrame(markets)
# filter to metropolitan statistical areas
msas = df.loc[df['location_type'] == 'MSA']
msa_parcl_ids = msas['parcl_id'].tolist()

#### LAST PRICE FOR EACH PARCL ID #####
# build url to get all last prices at once
last_price = 'https://api.realestate.parcllabs.com/v1/price_feed/latest'

for idx, msa in enumerate(msa_parcl_ids):
    qualifier = '&'
    if idx == 0:
        qualifier = '?'
    last_price += f'{qualifier}parcl_id={msa}'

# assign to msas dataframe
last_prices = requests.get(last_price, headers=header).json()
for parcl_id in msa_parcl_ids:
    msas.loc[msas['parcl_id'] == parcl_id, 'last_price'] = last_prices['price_feeds'][str(parcl_id)]['price']

##### FINANCIALS PER PARCL ID ######
# get financials of each parcl_id, including correlation coefficient w/30 year mortgage rates at 4 week lag
for parcl_id in msa_parcl_ids:
    url = f'https://api.realestate.parcllabs.com/v1/parcls/{parcl_id}/financials'
    response = requests.get(url, headers=header).json()
    msas.loc[msas['parcl_id'] == parcl_id, 'corr_coef_mortage_4_weeks'] = response['correlation_coefficient']['mortgage30us']['pricefeed_corr_coef_lag_4_weeks']

##### MEDIAN INCOME PER PARCL ID #####
# get median income for each metro area
for parcl_id in msa_parcl_ids:
    url = f'https://api.realestate.parcllabs.com/v1/place/{parcl_id}/demographics?category=income'
    response = requests.get(url, headers=header).json()
    tmp = response['income']
    for v in tmp:
        # grab most recent year
        if v['year'] == 2021:
            msas.loc[msas['parcl_id'] == parcl_id, 'median_income'] = v['value']

#### SAVE DATA FOR VIZ #####
msas.to_csv('~/Desktop/mortgages_with_income.csv', index=False)