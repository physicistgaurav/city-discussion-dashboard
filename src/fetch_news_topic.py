import requests
import os

def fetch_top_news_topic(city_name, api_key):

    query_params = {
        "sortBy": "top",
        "q": city_name,
        "apiKey": api_key
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

if __name__ == "__main__":
    api_key = os.getenv('NEWS_API_KEY')

    if not api_key:
        raise Exception("API key not found. Please set the NEWS_API_KEY environment variable.")
    
    city = input("Enter the name of the city: ")
    try:
        top_news = fetch_top_news_topic(city, api_key)
        print(f"Top 5 news topics in {city}:")
        for index, headline in enumerate(top_news, start=1):
            print(f"{index}. {headline}")
    except Exception as e:
        print(f"Error: {str(e)}")
