import requests
from bs4 import BeautifulSoup
from time import sleep
import json


def get_html(url, headers):
    sleep(2)
    r = requests.get(url, headers=headers)
    return r.text


def get_all_links(html):
    soup = BeautifulSoup(html, 'html.parser')

    tds = soup.find('div', class_='items-items-kAJAg').find_all('div', class_='iva-item-content-UnQQ4')

    links = []

    for td in tds:
        a = td.find('a').get('href')  # strings
        link = 'https://www.avito.ru/' + a
        links.append(link)

    return links


def get_page_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    try:
        info = soup.find('ul', class_='item-params-list').text.strip().replace('\xa0', ' ').replace(' \n', ',')
    except:
        info = '?'

    try:
        price = soup.find('span', class_='price-value-main').text.strip().replace('\xa0', ' ')
    except:
        price = '?'

    try:
        address = soup.find('span', class_='item-address__string').text.strip().replace('\xa0', ' ')
    except:
        address = '?'

    data = {
        'info': info,
        'price': price,
        'address': address
    }

    return data


def main():
    url = 'https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&p=1'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29'
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }

    all_links = get_all_links(get_html(url, headers))

    data = {}

    for i in range(1, len(all_links) + 1):
        data['i'] = get_page_data(get_html(all_links[i - 1], headers))

    with open('apartments', 'w') as file:
        json.dump(data, file, indent=3)


if __name__ == '__main__':
    main()
