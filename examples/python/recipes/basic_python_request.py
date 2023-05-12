import os
import requests

# Recommend storing your API Key outside of code, 
# in your bash_profile as an environment variable
api_key = os.getenv('parcl_labs_api_key')
# lets use cleveland as an example
parcl_id = 2899654 # Cleveland Metro Parcl ID

url = f"https://api.realestate.parcllabs.com/v1/place/{parcl_id}/demographics"

headers = {
    "accept": "application/json",
    "Authorization": f"{api_key}"
}

response = requests.get(url, headers=headers)

print(response.json()['income'])