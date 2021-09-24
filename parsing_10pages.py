import requests
from bs4 import BeautifulSoup

URL = 'https://www.avito.ru/sankt-peterburg/kvartiry?p='
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

# получаем количество страниц
# html_ = requests.get(URL + '1').text
# bs_ = BeautifulSoup(html_, 'html.parser')
#
# max_p = bs_.find_all('span', class_='pagination-item-JJq_j')
# pagination_list = []
# for p in max_p:
#     pagination_list.append(p.get_text())

# max_pages = int(pagination_list[-2])
for i in range(10):
    url = URL + str(i + 1)
    print('---------- страница № ' + str(i + 1) + ' ----------')
    html = requests.get(url).text
    bs = BeautifulSoup(html, 'html.parser')

    all_links = bs.find_all('a', class_='link-link-MbQDP link-design-default-_nSbv title-root-j7cja iva-item-title-_qCwt title-listRedesign-XHq38 title-root_maxHeight-SXHes')
    # all_prices = bs.find_all('span', class_='price-text-E1Y7h text-text-LurtD text-size-s-BxGpL')
    print('всего квартир на странице ' + str(len(all_links)))
    for link in all_links:
        # print('https://www.avito.ru/' + link['href'])
        print(link.get_text())
    print()
