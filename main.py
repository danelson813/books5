###################################
#            main.py
###################################
from log_helper import logger
from bs4 import BeautifulSoup as bs
import requests

logger.info('Logger has been started.')
results = []


def print_to_file(list_):
    with open('results.csv', 'a') as f:
        f.write(str(list_)+'\n')


def work_the_page(str_, results=None):
    base_url = 'https://books.toscrape.com/'
    if results is None:
        results = []
    res = requests.get(str_)
    soup = bs(res.text, 'lxml')

    books = soup.findAll('article')

    for book in books:
        title = book.find('h3').find('a').attrs['title']
        link = base_url + book.find('h3').find('a').attrs['href']
        price = book.find('p', class_='price_color').text[2:]
        result = {
            'title': title.replace(',', '-'),
            'price': price,
            'link': link
        }
        print_to_file(result)
        results.append(result)
    return results


if __name__ == "__main__":
    for page in range(1, 51):
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        results = work_the_page(url, results)
