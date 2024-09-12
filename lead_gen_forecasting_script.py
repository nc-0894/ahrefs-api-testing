import requests
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv('AHREFS_API_KEY')

# Function to fetch organic keywords for a competitor domain
def get_organic_keywords(domain, country='US', date='2024-09-10'):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }
    select_columns = 'best_position_url,keyword,volume,best_position,keyword_difficulty,sum_traffic,cpc'
    
    # Include the date parameter in the API URL
    api_url = f"https://api.ahrefs.com/v3/site-explorer/organic-keywords?target={domain}&country={country}&date={date}&select={select_columns}&output=json"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # This will raise an exception for 4xx/5xx responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching organic keywords for {domain}: {e}")
        return None

# Function to forecast traffic and revenue potential
def forecast_traffic(data, current_pos, target_pos):
    current_traffic = data.get('sum_traffic', 0)
    cpc_value = data.get('cpc', 0)

    improvement_factor = 2  # Example improvement factor
    potential_traffic = current_traffic * improvement_factor
    potential_value = potential_traffic * cpc_value
    
    return potential_traffic, potential_value

# Customize this: Add the domain of the prospect and the keyword
domain = "fodzyme.com"
keyword = "fructan intolerance"

# Fetch organic keyword data for the prospect's domain
data = get_organic_keywords(domain)

# Check if data is returned
if data:
    keywords = data.get('keywords', [])
    if keywords:
        best_keyword_data = keywords[0]  # Use the first keyword data
        current_pos = best_keyword_data.get('best_position', None)
        if current_pos is None:
            print(f"No ranking position data found for {domain}")
        else:
            target_pos = 3  # Define the target rank for forecasting
            potential_traffic, potential_value = forecast_traffic(best_keyword_data, current_pos, target_pos)
            print(f"If you ranked in position {target_pos} for '{keyword}', you could capture {potential_traffic:.2f} visits worth {potential_value:.2f} USD.")
    else:
        print(f"No keywords data found for {domain}")
else:
    print(f"No data returned for {domain}")
