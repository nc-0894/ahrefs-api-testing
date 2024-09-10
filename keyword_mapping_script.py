import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv('AHREFS_API_KEY')

# Function to fetch organic keywords for a specific URL or domain
def get_organic_keywords_for_url(url, country='us', date='2024-09-09'):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }
    select_columns = 'keyword,volume,best_position,keyword_difficulty,cpc,sum_traffic'
    api_url = f"https://api.ahrefs.com/v3/site-explorer/organic-keywords?target={url}&country={country}&date={date}&select={select_columns}&output=json"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching organic keywords for {url}: {e}")
        return None


# List of URLs on your domain
urls = [
    'https://linkflow.ai/saas-seo-agency/',
    'https://linkflow.ai/content-strategy-services/',
    'https://linkflow.ai/link-building-services/',
    'https://linkflow.ai/video-seo-services/',
    'https://linkflow.ai/saas-content-marketing-services/'
]

# Dictionary to store URL to keyword mappings
url_keyword_map = {}

for url in urls:
    data = get_organic_keywords_for_url(url)
    if data:
        keywords = data.get('keywords', [])
        best_keyword = keywords[0]['keyword'] if keywords else 'No suitable keyword found'
        url_keyword_map[url] = best_keyword

# Convert the map to a DataFrame for easier handling
df = pd.DataFrame(list(url_keyword_map.items()), columns=['URL', 'Best Keyword'])

# Print the results
print(df)

# Optionally, save the results to a CSV file
df.to_csv('url_keyword_mapping.csv', index=False)
