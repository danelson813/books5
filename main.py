###################################
#            main.py
###################################
"""
SCRAPS A WEBSITE FOR INFORMATION ON BOOKS AND SAVES INFO SEVERAL WAYS

THIS IS A PROOF OF CONCEPT PROGRAM. IT TRIES TO DO SEVERAL THINKS,
NOT ALL ARE NECESSARY, IT SHOWS HOW TO DO SEVERAL THINGS
"""
from log_helper import logger
from bs4 import BeautifulSoup as bs
import requests
import sqlite3

logger.info('Logger has been started.')
results = []


def print_to_file(list_):
    with open('results.csv', 'a') as f:
        f.write(str(list_) + '\n')


def work_the_page(str_: str, results_: list = None):
    base_url = 'https://books.toscrape.com/'
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
        results_.append(result)
    return results_


def save_the_books(results_):
    connection = sqlite3.connect("books.db")
    c = connection.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS books
        (title TEXT, price text, link TEXT)
    ''')
    c.executemany('''INSERT INTO books(
                  title, 
                  price, 
                  link) 
                  VALUES (:title,:price,:link)''',
                  results_)
    connection.commit()
    connection.close()


if __name__ == "__main__":
    for page in range(1, 51):
        logger.info(f"Working on page {page}.")
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        results = work_the_page(url, results)

    save_the_books(results)
