from fetch_news import fetch
from pretify_news import news_data

def news(count):
    raw_data=fetch(count)
    data=news_data(raw_data)
    return data

