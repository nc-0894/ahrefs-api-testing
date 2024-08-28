import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv('AHREFS_API_KEY')

# Function to fetch organic keywords for a specific URL
def get_keywords_for_url(url):
    api_url = f"https://api.ahrefs.com/v3/site-explorer/keywords"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {url}: {e}")
        return None

# Function to fetch related keywords for a given keyword (secondary search)
def get_related_keywords(keyword):
    api_url = f"https://api.ahrefs.com/v3/related_keywords"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching related keywords for {keyword}: {e}")
        return None

# Function to determine the best keyword based on volume, difficulty, and URL slug
def find_best_keyword(keywords, url_slug):
    best_keyword = None
    best_score = float('-inf')
    
    for kw in keywords:
        volume = kw.get('volume', 0)
        difficulty = kw.get('difficulty', 100)  # Assume max difficulty if not provided
        keyword_text = kw.get('keyword', '')

        # Simple scoring formula: prioritize high volume and low difficulty
        score = volume - (difficulty * 10)  # Adjust the weighting as needed

        # Include a factor for matching the keyword with the URL slug topic
        if url_slug in keyword_text.lower():
            score += 1000  # Boost score if the keyword matches the URL slug topic

        if score > best_score:
            best_score = score
            best_keyword = keyword_text
    
    return best_keyword

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
    # Extract the URL slug (the part after the last '/')
    url_slug = url.split('/')[-1].replace('-', ' ')
    
    data = get_keywords_for_url(url)
    if data:
        keywords = data.get('keywords', [])
        best_keyword = find_best_keyword(keywords, url_slug)
        
        # If no suitable keyword found, perform secondary search using phrase match
        if not best_keyword:
            print(f"No suitable keyword found for {url}. Searching for related keywords...")
            related_keywords_data = get_related_keywords(url_slug)
            if related_keywords_data:
                related_keywords = related_keywords_data.get('phrases', [])
                best_keyword = find_best_keyword(related_keywords, url_slug)
        
        url_keyword_map[url] = best_keyword or 'No suitable keyword found'

# Convert the map to a DataFrame for easier handling
df = pd.DataFrame(list(url_keyword_map.items()), columns=['URL', 'Best Keyword'])

# Print the results
print(df)

# Optionally, save the results to a CSV file
df.to_csv('url_keyword_mapping.csv', index=False)
