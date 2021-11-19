import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://www.avito.ru/sankt-peterburg/kvartiry?p='
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


# количество страниц
def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='pagination-item-JJq_j')  # строка пагинации
    if pagination:
        return int(pagination[-2].get_text())  # возвращает количество страниц
    else:
        return 1  # или 1, тк нет строки пагинации == 1 страница


def write_csv(i):
    with open('parsed_file.scv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(i)


# пытаюсь брать информацию после перехода по каждой ссылке
# def get_each_url(html, number_of_pages=1):
#     html = get_html(URL)
#     links = []
#     for i in range(number_of_pages):
#         url = URL + str(i + 1)
#         html = requests.get(url).text
#         soup = BeautifulSoup(html, 'html.parser')
#         # links = soup.find_all('div', class_='iva-item-titleStep-_CxvN').get('href')
#         all_links = soup.find_all('a',
#                                   class_='link-link-MbQDP link-design-default-_nSbv title-root-j7cja iva-item-title-_qCwt title-listRedesign-XHq38 title-root_maxHeight-SXHes')
#         for link in all_links:
#             links.append(link.get_text())
#     return links


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_info = soup.find_all('div', class_='iva-item-body-R_Q9c')

    homes = []
    for info in all_info:
        homes.append({
            # 'info': info.get_text().replace('\xa0', ' '),
            'type': info.get_text().split(',')[0].replace('\xa0', ' '),
            'area': info.get_text().split(', ')[1].replace('\xa0', ' '),
            'floor': info.get_text().split(', ')[2:][0].split('.')[0].replace('\xa0', ' ') + '.',
            'price': info.get_text().split(', ')[2].split('.')[1].split('₽')[0].replace('\xa0', ' ') + '₽',
            # 'address': info.get_text().split(', ')[2].split('.')[1].split('₽')[1].replace('\xa0', ' '),  # неправильно выводит адрес
        })
    return homes


def parse():
    html = get_html(URL)
    # if html.status_code == 200:
    pages_count = get_pages_count(html.text)
    data = []
    print(f'{pages_count} страниц всего', end='\n\n')
    for i in range(2):
        url = URL + str(i + 1)
        print('---------- страница № ' + str(i + 1) + ' ----------')
        html = requests.get(
            url).text  # get_each_url -------------------------------------------------------------------------
        # try:
        data += get_content(html)
        # except:
        #     pass
        print(data)
        print(f'Получено {len(data)} квартир')
        # return data
    # else:
    #     print('Error with server')


parse()

# def main():
#     parsed_data = parse()
#     for i in parsed_data:
#         write_csv(i)
#
#
# if __name__ == '__main__':
#     main()
