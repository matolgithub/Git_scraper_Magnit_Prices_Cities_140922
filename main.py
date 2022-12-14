import datetime
import csv
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def collect_data(city_code='2398'):
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    ua = UserAgent()

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'User-Agent': ua.random
    }

    cookies = {
        'mg_geo_id': f'{city_code}'
    }

    response = requests.get(url='https://magnit.ru/promo/', headers=headers, cookies=cookies)

    # with open('index.html', 'w') as file:
    #     file.write(response.text)
    #
    # with open('index.html') as file:
    #     pprint(file.read())

    soup = BeautifulSoup(response.text, 'lxml')

    city = soup.find('a', class_='header__contacts-link header__contacts-link_city').text.strip()
    cards = soup.find_all('a', class_='card-sale card-sale_catalogue')
    # goods = soup.find('div', class_='card-sale__title').find('p').text.strip()
    print(city, len(cards))
    # print(goods)

    data = []
    for card in cards:
        card_title = card.find('div', class_='card-sale__title').text.strip()
        # print(card_title)
        try:
            card_discount = card.find('div', class_='card-sale__discount').text.strip()
            # print(card_discount)
        except AttributeError:
            # print("Not success")
            continue

        card_price_old_integer = card.find('div', class_='label__price_old').find('span',
                                                                                  class_='label__price-integer').text.strip()
        card_price_old_decimal = card.find('div', class_='label__price_old').find('span',
                                                                                  class_='label__price-decimal').text.strip()
        card_old_price = f'{card_price_old_integer}.{card_price_old_decimal}'

        card_price_integer = card.find('div', class_='label__price_new').find('span',
                                                                              class_='label__price-integer').text.strip()
        card_price_decimal = card.find('div', class_='label__price_new').find('span',
                                                                              class_='label__price-decimal').text.strip()
        card_price = f'{card_price_integer}.{card_price_decimal}'

        card_sale_date = card.find('div', class_='card-sale__date').text.strip().replace('\n', ' ')
        # print(card_sale_date)

        data.append(
            [card_title, card_discount, card_old_price, card_price, card_sale_date]
        )

    with open(f'{city}_{cur_time}.csv', 'w', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(
            ["??????????????", "???????????? ????????", "?????????? ????????", "?????????????? ????????????", "?????????? ??????????"]
        )
        writer.writerows(data)
        print(f'???????? "{city}_{cur_time}.csv" ?????????????? ??????????????!')


def main():
    collect_data('2398')


if __name__ == "__main__":
    collect_data()
