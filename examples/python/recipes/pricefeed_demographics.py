import os
import requests

import pandas as pd


PARCL_LABS_API_KEY = os.getenv('PARCL_LABS_API_KEY')

PARCL_ID = 2900187 # new york metro area

# pass in parcl_id into the url structure
url = f'https://api.realestate.parcllabs.com/v1/place/{PARCL_ID}/demographics'

headers = {
    'Authorization': PARCL_LABS_API_KEY
}


response = requests.get(
    url, 
    headers=headers
)

r_json = response.json()

wanted_vars = [
    'pop_female_never_married',
    'pop_male_never_married',
    'pop_female_divorced',
    'pop_male_divorced',
    'pop_male_married',
    'pop_female_married',
    'female_single_population',
    'female_taken_population',
    'male_single_population',
    'male_taken_population',
    'pop_male',
    'pop_female'
]

tmp = {}

for v in r_json['population']:
    if v['year'] == 2021 and v['variable'] in wanted_vars:
        tmp[v['variable']] = v['value']

total_male_pop = (tmp['pop_male_married']+tmp['pop_male_divorced'])
total_female_pop = (tmp['pop_female_married']+tmp['pop_female_divorced'])
percent_male_divorce = tmp['pop_male_divorced']/total_male_pop
percent_female_divorce = tmp['pop_female_divorced']/total_female_pop
total_divorce_rate = (tmp['pop_male_divorced'] + tmp['pop_female_divorced'])/(total_male_pop + total_female_pop)
print(f"{total_divorce_rate:.1%}")
# 14.4%