import requests
from bs4 import BeautifulSoup

#end URL
URL = 'https://auto.ria.com/uk/newauto/marka-jeep/'
# headers are needed to prevent the browser from being banned and considered a bot
HEADERS = {}
HOST = 'https://auto.ria.com'


def get_html(url, params=None): # params used for pagination, filter, etc.
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser') #html.parser need, because soap works also with xml and other formats
    items = soup.find_all('div', class_='proposition') #find all items with tag = a

    cars = [] #in this list we collect parsed items
    for item in items:
        uah_price = item.find('span', class_='size13')
        if uah_price:
            uah_price = uah_price.get_text().replace('', '')
        else:
            uah_price = 'No uah price'
        cars.append({
            'title': item.find('strong', class_='link').get_text(strip=True), #strip used for space deletion
            'link': HOST + item.find('a', class_='proposition_link').get('href'),
            'usd_price': item.find('span', class_='green').get_text(),
            'uah_price': uah_price,
            'city': item.find('div', class_='size13').find_next('strong').get_text()
        })

    print(cars)

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error')

parse()
