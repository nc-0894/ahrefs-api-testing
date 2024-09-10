import requests
import os
import pandas as pd
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv('AHREFS_API_KEY')

# Function to fetch organic keywords for a competitor domain
def get_organic_keywords(domain, country='us', date='2024-09-09'):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }
    select_columns = 'keyword,volume,best_position,keyword_difficulty'
    api_url = f"https://api.ahrefs.com/v3/site-explorer/organic-keywords?target={domain}&country={country}&date={date}&select={select_columns}&output=json"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching organic keywords for {domain}: {e}")
        return None
    
# Function to fetch backlinks for a competitor domain
def get_backlinks(domain, country='us', date='2024-09-09'):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }
    select_columns = 'backlink,anchor_text,referring_domain'
    api_url = f"https://api.ahrefs.com/v3/site-explorer/all-backlinks?target={domain}&country={country}&date={date}&select={select_columns}&output=json"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching backlinks for {domain}: {e}")
        return None

# Function to fetch top pages for a competitor domain
def get_top_pages(domain, country='us', date='2024-09-09'):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }
    select_columns = 'page,organic_traffic,backlinks'
    api_url = f"https://api.ahrefs.com/v3/site-explorer/top-pages?target={domain}&country={country}&date={date}&select={select_columns}&output=json"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching top pages for {domain}: {e}")
        return None

# Test with one competitor
competitor = 'linkflow.ai'  # for testing purposes
country = 'us'
date = '2024-09-09'

print(f"Fetching data for {competitor}...")

# Fetch organic keywords for this competitor
organic_keywords = get_organic_keywords(competitor, country, date)
if organic_keywords:
    df_keywords = pd.DataFrame(organic_keywords.get('keywords', []))
    df_keywords.to_csv(f'{competitor}_organic_keywords.csv', index=False)
    print(f"Organic keywords saved for {competitor}")
else:
    print("No organic keywords found")

# Fetch backlinks for this competitor
backlinks = get_backlinks(competitor, country, date)
if backlinks:
    df_backlinks = pd.DataFrame(backlinks.get('backlinks', []))
    df_backlinks.to_csv(f'{competitor}_backlinks.csv', index=False)
    print(f"Backlinks saved for {competitor}")
else:
    print("No backlinks found")

# Fetch top pages for this competitor
top_pages = get_top_pages(competitor, country, date)
if top_pages:
    df_top_pages = pd.DataFrame(top_pages.get('pages', []))
    df_top_pages.to_csv(f'{competitor}_top_pages.csv', index=False)
    print(f"Top pages saved for {competitor}")
else:
    print("No top pages found")
