from dotenv import load_dotenv
import os
import requests

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
NEWS_TOKEN = os.getenv('NEWS_TOKEN')

def get_articles(keyword):
    if keyword == 'News':
        link = 'https://newsapi.org/v2/top-headlines?'
    else:
        link = 'https://newsapi.org/v2/everything?'
    # link = 'https://newsapi.org/v2/everything?'
    url = ('{link}'
		'q={keyword}-yahoo-Yahoo&'

		'sortBy=popularity&'
		'language=en&'
		'excludeDomains=consent.yahoo.com&'
		'apiKey={token}'.format(link=link,keyword=keyword, token=NEWS_TOKEN))

    response = requests.get(url)
    print(response.json()['status'])

    return response.json()

# get_articles("News")