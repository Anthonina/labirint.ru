import requests
import time
import json
from bs4 import BeautifulSoup


def get_html(url):
    response_url = requests.get(url)
    return response_url.text

def clear_string(in_string, find = ['Масса:', 'Размеры:', 'Страниц:', 'Издательство:', 'ISBN:', 'Цена', 'ID товара:']):
    for f in find:
        in_string = in_string.replace(f, '').strip()

    return in_string


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
        goods_data[attr_name] = clear_string(data.text.replace('\n', ' '))


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

    working_file_json = 'labirint_json.txt'
    file_labirint_json = open(working_file_json, mode = 'w', encoding = 'utf8')

    #labirint_url_array = ['https://www.labirint.ru/office/10002/', 'https://www.labirint.ru/office/10009/']
    with open('labirint_url.txt') as file:
        labirint_url_array = [row.strip() for row in file]

    labirint_array_json = []

    index = 0
    length = len(labirint_url_array)
    for url_labirint in labirint_url_array:
        html = get_html (url_labirint)
        page_data = get_page_data(html)
        labirint_array_json.append(page_data)
        index += 1
        print("Parsed {} of {} pages".format(index, length))

        if index == 10:
            break

        if index < length:
            time.sleep(3)
        
    json.dump(labirint_array_json, file_labirint_json, ensure_ascii=False)
    
    file_labirint_json.close()

    print("Parsing complete!")


        #print(page_data)
        #print('--------------------')
        

if __name__ == '__main__':
    main()