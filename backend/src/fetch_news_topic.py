import requests
import os
import json
from datetime import datetime, timedelta

def fetch_top_news_topic(city_name ):

    api_key = os.getenv('NEWS_API_KEY')
    if not api_key:
        raise Exception("API key not found. Please set the NEWS_API_KEY environment variable.")
    query_params = {
        "sortBy": "relevancy",
        "q": city_name,
        "apiKey": api_key,
        "language": "en",
    }

    api_url = "https://newsapi.org/v2/everything"
    
    response = requests.get(api_url, params=query_params)
    news_data = response.json()
    
    if news_data.get('status') == 'ok':
        articles = news_data.get('articles', [])[:5]
        headlines = [article['title'] for article in articles]
        return headlines
    else:
        raise Exception("Failed to fetch news topics")

def save_topics_to_file(topics, city_name):
    sanitized_city_name = city_name.replace(" ", "_").lower()
    filename = f"data/{sanitized_city_name}.json"
    with open(filename, 'w') as f:
        json.dump(topics, f, indent=4)

if __name__ == "__main__":
    
    city = input("Enter the name of the city: ")
    try:
        top_news = fetch_top_news_topic(city)
        save_topics_to_file(top_news, city)
        print(f"Top 5 news topics in {city}:")
        for index, headline in enumerate(top_news, start=1):
            print(f"{index}. {headline}")
    except Exception as e:
        print(f"Error: {str(e)}")
