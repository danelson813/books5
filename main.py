###################################
#            main.py
###################################
from log_helper import logger
from bs4 import BeautifulSoup as bs
import requests

logger.info('Logger has been started.')
base_url = 'https://books.toscrape.com/'

url = 'https://books.toscrape.com/'
res = requests.get(url)
soup = bs(res.text, 'lxml')

books = soup.findAll('article')
logger.info(f'length of books is {len(books)}')

results = []
for book in books[:2]:
    title = book.find('h3').find('a').attrs['title']
    link = base_url + book.find('h3').find('a').attrs['href']
    price = book.find('p', class_='price_color').text[2:]
    result = {
        'title': title,
        'price': price,
        'link': link
    }
    results.append(result)
# TODO: paginate and add a df
