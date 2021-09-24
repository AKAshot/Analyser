import requests
from bs4 import BeautifulSoup

URL = 'https://www.avito.ru/sankt-peterburg/kvartiry?p='
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='link-link-MbQDP link-design-default-_nSbv title-root-j7cja iva-item-title-_qCwt title-listRedesign-XHq38 title-root_maxHeight-SXHes')
    # items = soup.find_all('div', class_='iva-item-body-R_Q9c')

    cars = []
    for item in items:
        cars.append({
            'type': item.get_text().split(',')[0].replace('\xa0', ' '),
            'area': item.get_text().split(',')[-2].replace('\xa0', ' '),
            'floor': item.get_text().split(',')[-1].replace('\xa0', ' ')
        })
    print(cars)
    print(len(cars))


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error')


parse()
