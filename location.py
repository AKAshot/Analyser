import requests
from time import sleep
from bs4 import BeautifulSoup
import json


# берем html по url
def get_html(url, headers=None) -> str:
    sleep(10)
    r = requests.get(url, headers=headers)
    return r.text


# берем количество всех страниц раздела
def get_pages_count(html) -> int:
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='pagination-item-JJq_j')  # строка пагинации
    if pagination:
        return int(pagination[-2].get_text())  # возвращает количество страниц
    else:
        return 1  # или 1, тк нет строки пагинации == 1 страница

    
# переходим на каждую страницу пагинации и берем ссылки на все объявления, которые на ней
def get_all_links(html):
    soup = BeautifulSoup(html, 'html.parser')

    tds = soup.find('div', class_='items-items-kAJAg').find_all('div', class_='iva-item-content-UnQQ4')

    links = []

    for td in tds:
        a = td.find('a').get('href')  # strings
        link = 'https://www.avito.ru/' + a
        links.append(link)

    return links


# проверка на наличие конкретной информации (перечень параметров у объявлений разнится, он не фиксирован; так, например, не у каждого 
#объявления есть информация о наличии балкона)
def check(arr, sub):
    k = 'no info'
    for i in arr:
        if sub in i:
            k = i.split(': ')[-1]
    return k


# переходим по каждой ссылке на квартиру и передаем html страницы парсеру, берем нужную информацию и составляем словарь/объект квартиры
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
    # задаем "константы"
    URL = 'https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&p='
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    params = ['Этаж', 'Количество комнат', 'Тип комнат', 'Общая площадь', 'Ремонт', 'Отделка', 'Санузел',
              'Балкон или лоджия', 'Вид из окон', 'Дополнительно']
    # если мы попадаем на сервер (нас не заблокировали), то выполняем код
    if requests.get(URL + '1', headers=headers).status_code == 200:
        # берем html главной (первой) страницы с объявлениями
        html = get_html(URL, headers)
        # получаем количество страниц
        pages_count = get_pages_count(html)
        # здесь будем хранить все ссылки на объявления
        all_links = []
        
        # итерируемся по всем страницам и берем ссылки с каждой из них
        for i in range(1, pages_count + 1):
            html = get_html(URL + 'i', headers)
            try:
                all_links.extend(get_all_links(html))
            except:
                pass
        
        # список словарей всех квартир
        data = []
        
        # переходим по каждой ссылке из списка ссылок, составляем словарь объявления и вносим его в список словарей
        for i in range(len(all_links)):
            html = get_html(all_links[i], headers)
            data.append(get_page_data(html, all_links[i], params))
        
        sleep(30)
        
        # записываем данные в json-файл
        write(data, 'apartments.json')

        print('successfully!!!')
        print(len(data))

    else:
        print('Error with server')


if __name__ == '__main__':
    main()
