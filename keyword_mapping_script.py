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
    select_columns = 'keyword,volume,best_position,keyword_difficulty,best_position_url'
    api_url = f"https://api.ahrefs.com/v3/site-explorer/organic-keywords?target={url}&country={country}&date={date}&select={select_columns}&output=json"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching organic keywords for {url}: {e}")
        return None

# Function to fetch related keywords for additional research
def get_related_keywords(keyword, country='us'):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }
    select_columns = 'keyword,volume,keyword_difficulty'
    api_url = f"https://api.ahrefs.com/v3/keywords-explorer/related-terms?target={keyword}&country={country}&select={select_columns}&output=json"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching related keywords for {keyword}: {e}")
        return None

# Scoring function based on volume, difficulty, and relevance to the URL slug
def find_best_keyword(keywords, url_slug, target_url):
    best_keyword = None
    best_volume = 0
    best_difficulty = 100
    best_score = float('-inf')
    
    for kw in keywords:
        volume = kw.get('volume', 0)
        difficulty = kw.get('keyword_difficulty', 100)  # Assume max difficulty if not provided
        keyword_text = kw.get('keyword', '')
        ranking_url = kw.get('best_position_url', '')  # Get the URL associated with the keyword

        # Only consider keywords that are ranking for the specific URL
        if ranking_url == target_url:
            # Scoring formula: prioritize high volume, low difficulty, and relevance to the URL slug
            score = volume - (difficulty * 10)
            if url_slug in keyword_text.lower():
                score += 1000  # Boost score if the keyword matches the URL slug topic

            if score > best_score:
                best_score = score
                best_keyword = keyword_text
                best_volume = volume
                best_difficulty = difficulty
    
    return best_keyword, best_volume, best_difficulty

# List of URLs on your domain. Update accordingly.
urls = [
    'https://linkflow.ai/saas-seo-agency/',
    'https://linkflow.ai/content-strategy-services/',
    'https://linkflow.ai/link-building-services/',
    'https://linkflow.ai/video-seo-services/',
    'https://linkflow.ai/saas-content-marketing-services/'
]

# Dictionary to store URL to keyword mappings
url_keyword_map = []

for url in urls:
    url_slug = url.split('/')[-1].replace('-', ' ')  # Extract URL slug
    organic_data = get_organic_keywords_for_url(url)
    
    if organic_data:
        keywords = organic_data.get('keywords', [])
        best_keyword, best_volume, best_difficulty = find_best_keyword(keywords, url_slug, url) #add best_position
        
        # If no suitable keyword found, perform secondary search using related terms
        if not best_keyword:
            print(f"No suitable keyword found for {url}. Searching for related terms...")
            if keywords:
                first_keyword = keywords[0].get('keyword', '')  # Use first keyword for related terms
                related_keywords_data = get_related_keywords(first_keyword)
                if related_keywords_data:
                    related_keywords = related_keywords_data.get('keywords', [])
                    best_keyword, best_volume, best_difficulty = find_best_keyword(related_keywords, url_slug, url)

        url_keyword_map.append({
            'URL': url,
            'Best Keyword': best_keyword or 'No suitable keyword found',
            'Keyword Volume': best_volume,
            'Keyword Difficulty': best_difficulty
        })

# Convert the map to a DataFrame for easier handling
df = pd.DataFrame(url_keyword_map)

# Print the results
print(df)

# Optionally, save the results to a CSV file
df.to_csv('url_keyword_mapping.csv', index=False)
