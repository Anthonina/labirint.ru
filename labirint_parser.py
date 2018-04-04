import requests
from bs4 import BeautifulSoup


def get_html(url):
    response_url = requests.get(url)
    return response_url.text


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    goods_data = {}

    characteristics = soup.find('div', id = 'product')

    try:
        bread_crumbs = characteristics.find('div', id = 'thermometer-books').text.replace(u'\xa0', u' ')
    except:
        bread_crumbs = ''
    
    goods_data['bread_crumbs'] = bread_crumbs

    try:
        title = characteristics.find('div', id = 'product-title').find('h1').text
    except:
        title = ''
    
    goods_data['title'] = title

    try:
        product_data = characteristics.find('div', id = 'product-specs').findAll('div', {'class': [
                                                                                                    'publisher',
                                                                                                    'authors',
                                                                                                    'buying-price',
                                                                                                    'buying-priceold',
                                                                                                    'buying-pricenew',
                                                                                                    'articul',
                                                                                                    'isbn',
                                                                                                    'pages2',
                                                                                                    'weight',
                                                                                                    'dimensions'
                                                                                                  ]
                                                                                        }
                                                                                )
    except:
        product_data = []    

    for data in product_data:
        attr_name = data['class'][0]
        goods_data[attr_name] = data.text.replace('\n', ' ')


    try:
        product_data_2 = characteristics.find('div', id = 'product-right-column').findAll('div', {'id': [
                                                                                                        'product-about',
                                                                                                        'rate'
                                                                                                        ]
                                                                                                }
                                                                                        )
    except:
        product_data_2 = ''

    for data_2 in product_data_2:
        attr_name_2 = data_2['id']
        goods_data[attr_name_2] = data_2.text.replace('\n', ' ')

    return goods_data


def main():
    url = 'https://www.labirint.ru/office/635306/'
    html = get_html (url)
    page_data = get_page_data(html)

    print(page_data)

if __name__ == '__main__':
    main()