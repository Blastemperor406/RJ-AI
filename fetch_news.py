import requests
import json
from datetime import datetime, timedelta

def fetch(count):
    loc_url = f"https://api.worldnewsapi.com/geo-coordinates?location=Bengaluru%2C%20India"
    # print("Check1")
    headers = {
        'x-api-key': "4fc4b886d99145b2af8c25401617525d"
    }
    now = datetime.utcnow()
    earliest_publish_date = now - timedelta(hours=24)
    formatted_date = earliest_publish_date.strftime('%Y-%m-%d')
    response = requests.get(loc_url, headers=headers)
    loc=response.json()
    #print(loc)
    if response.status_code == 200:
        url = (f"https://api.worldnewsapi.com/search-news?"
               f"location-filter={loc['latitude']},{loc['longitude']},50&"
               f"language=en&earliest-publish-date={formatted_date}&categories=politics,sports,business,technology,health,lifestyle&max-sentiment=-0.5&number={count}")  # For highly negative news

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            negative_news = response.json()

        url = (f"https://api.worldnewsapi.com/search-news?"
               f"location-filter={loc['latitude']},{loc['longitude']},50&"
               f"language=en&earliest-publish-date={formatted_date}&categories=politics,sports,business,technology,health,lifestyle&min-sentiment=0.5&number={count}")  # For highly positive news

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            positive_news = response.json()

        # Combine results from both queries
        polarizing_news = {
            'news': negative_news['news'] + positive_news['news']
        }

        return polarizing_news
    if response.status_code == 200:
        url = f"https://api.worldnewsapi.com/search-news?location-filter={loc['latitude']},{loc['longitude']},100&language=en&earliest-publish-date={formatted_date}&categories=politics,sports,business,technology,health,lifestyle&min-sentiment=-0.5&number={2*count}"
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            #print("Check3")
            #print(response)
            return response.json()
        else:
            #print(f"Failed to fetch news")
            return None
    else:
       # print(response.status_code )
        #print(f"Failed to fetch location")
        return None

