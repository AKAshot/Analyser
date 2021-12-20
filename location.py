import requests
from time import sleep
from bs4 import BeautifulSoup
import json


def get_html(url, headers=None) -> str:
    sleep(10)
    r = requests.get(url, headers=headers)
    return r.text


def get_pages_count(html) -> int:
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='pagination-item-JJq_j')  # строка пагинации
    if pagination:
        return int(pagination[-2].get_text())  # возвращает количество страниц
    else:
        return 1  # или 1, тк нет строки пагинации == 1 страница


def get_all_links(html):
    soup = BeautifulSoup(html, 'html.parser')

    tds = soup.find('div', class_='items-items-kAJAg').find_all('div', class_='iva-item-content-UnQQ4')

    links = []

    for td in tds:
        a = td.find('a').get('href')  # strings
        link = 'https://www.avito.ru/' + a
        links.append(link)

    return links


def check(arr, sub):
    k = 'no info'
    for i in arr:
        if sub in i:
            k = i.split(': ')[-1]
    return k


def get_page_data(html, link=None, params=None):
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
    try:
        latitude = soup.find('div', class_='b-search-map expanded item-map-wrapper js-item-map-wrapper').get(
            'data-map-lat')
    except:
        latitude = '?'
    try:
        longitude = soup.find('div', class_='b-search-map expanded item-map-wrapper js-item-map-wrapper').get(
            'data-map-lon')
    except:
        longitude = '?'

    info = info.split(', ')

    data = {param: check(info, param) for param in params}

    extra_data = {
        'Цена': price,
        'Адресс': address,

        'Широта': latitude,
        'Долгота': longitude,

        'Ссылка': link
    }

    data |= extra_data

    return data


# запись в json
def write(data, filename):
    data = json.dumps(data)
    data = json.loads(str(data))
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    URL = 'https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&p='
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    params = ['Этаж', 'Количество комнат', 'Тип комнат', 'Общая площадь', 'Ремонт', 'Отделка', 'Санузел',
              'Балкон или лоджия', 'Вид из окон', 'Дополнительно']

    if requests.get(URL + '1', headers=headers).status_code == 200:
        html = get_html(URL, headers)
        pages_count = get_pages_count(html)
        all_links = []

        for i in range(1, pages_count + 1):
            html = get_html(URL + 'i', headers)
            all_links.extend(get_all_links(html))

        data = {}

        for i in range(pages_count):
            html = get_html(all_links[i], headers)
            data[i] = get_page_data(html, all_links[i], params)

        write(data, 'apartments.json')

        print('successfully!!!')
        print(len(data))

    else:
        print('Error with server')


if __name__ == '__main__':
    main()
