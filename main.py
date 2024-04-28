import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.cnbc.com/quotes/NVDA'

response = requests.get(url, timeout=10)

soup = BeautifulSoup(response.content, 'html.parser')

div_stock = soup.find('div', class_='QuoteStrip-lastTimeAndPriceContainer')
div_stock_summary = soup.find('ul', class_='Summary-data Summary-stock')
quote_news_list = soup.find('ul', class_='LatestNews-list')

children_div_stock = div_stock.find_all()
children_div_stock_summary = div_stock_summary.find_all('li')
children_quote_news_list = quote_news_list.find_all('li')
headlines = []

for child in children_quote_news_list:
    headline_wrapper_quote_news = child.find('div', class_='LatestNews-headlineWrapper')
    headline = headline_wrapper_quote_news.find('a', class_='LatestNews-headline').text
    headlines.append(headline)

data = {}

for child in children_div_stock:
    classname = ' '.join(child.get('class')) if child.get('class') else 'None'
    if classname == 'QuoteStrip-lastPrice':
        data['share_price'] = child.text.strip()
    elif classname == 'QuoteStrip-changeUp':
        change_up = child.text.strip().split(' ')
        data['share-change-up'] = change_up[0]
        data['share-change-down'] = change_up[1].strip('()')

for child in children_div_stock_summary:
    key = child.find('span', class_='Summary-label').text
    value = child.find('span', class_='Summary-value').text
    data[key] = value

data['news'] = headlines

json_object = json.dumps(data, indent=4)

print(json_object)