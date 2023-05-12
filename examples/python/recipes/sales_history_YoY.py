"""
To get started with the Parcl Labs API, please follow the quick start
guide to get your API key: 

https://docs.parcllabs.com/docs/quickstart
"""

import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

PARCL_LABS_API_KEY = os.getenv('parcl_labs_api_key') 
PARCL_ID = 2900187 # new york market

# pass in parcl_id into the url structure, replace with prod URL
url = f'https://api.realestate.dev.parcllabs.com/v1/sales/{PARCL_ID}/history'

# authorize
header = {
    'Authorization': PARCL_LABS_API_KEY
}

response = requests.get(
    url,
    headers=header
)

# convert the json response into a pandas dataframe
sales = pd.DataFrame(response.json()['historical_sales'])

# Convert the 'date' column to a datetime object, extract the year, and month-day
sales['date'] = pd.to_datetime(sales['date'])
sales['year'] = sales['date'].dt.year 
sales['day_of_year'] = sales['date'].dt.strftime('%m-%d')
sales['rolling_avg'] = sales['sales_30_day'].rolling(window=7).mean()

sales = sales.sort_values(by='day_of_year', ascending=True)

# Create a time series chart using matplotlib
plt.style.use('seaborn-v0_8-darkgrid')
fig, ax = plt.subplots(figsize=(10, 6))

years = sorted(sales['year'].unique())

for y in years:
    ax.plot(sales[(sales['year'] == y)]['day_of_year'],
            sales[(sales['year'] == y)]['rolling_avg'],
            label = y)
                
#format the visualization
ax.legend()
ax.set_xlabel('Date')
ax.set_ylabel('Rolling 30 Day Sales')
ax.set_title('Year Over Year Sales: New York MSA')
ax.grid(False)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

plt.show()