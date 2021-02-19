import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://auto.ria.com/uk/newauto/marka-toyota/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='mhide')
    if pagination:
        return int(pagination[-1].get_text()) # take last page number
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser') #html.parser need, because soap works also with xml and other formats
    items = soup.find_all('div', class_='proposition') #find all items with tag = a

    cars = []
    for item in items:
        uah_price = item.find('span', class_='size15')
        if uah_price:
            uah_price = uah_price.get_text().replace(' • ', '')
        else:
            uah_price = 'No UAH price'
        cars.append({
            'title': item.find('strong', class_='link').get_text(strip=True), #strip used for space deletion
            'link': HOST + item.find('a', class_='proposition_link').get('href'),
            'usd_price': item.find('span', class_='green').get_text(),
            'uah_price': uah_price,
            'city': item.find('div', class_='size13').find_next('strong').get_text()
        })
    return cars


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Brand', 'Link', 'Price in USD', 'Price in UAH', 'City']) # columns names
        for item in items:
            writer.writerow([item['title'], item['link'], item['usd_price'], item['uah_price'], item['city']])


def parse():
    URL = input('Enter URL: ')
    URL = URL.strip() #delete space in entered link
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1): #pages taken from URL for 2nd+ page
            print(f'Parse {page} of {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text)) #extend cars after iteration
        save_file(cars, FILE) #save file
        print(f'Total {len(cars)} cars')
        os.startfile(FILE) # open file after parse
    else:
        print('Error')


parse()
