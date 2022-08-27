import os
from datetime import datetime
from bs4 import BeautifulSoup as bs
from time import sleep
import requests
from dotenv import load_dotenv
import re


load_dotenv()
URLS = [
    'avtograd_moskva',
    'maklermotors_moskva',
    'genzes_moskva',
    'auto_expert_moskva',
    'pulsar_motors_moskva',
    'avtolider_varshavka_moskva',
    'prime_moskva'
]
CHAT = '@calls_from_office'
PRE_URL = 'https://auto.ru/diler/cars/used/'
TLG_TOKEN = os.getenv('TOKEN')
HEADERS = {'accept': '*/*', 'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 '
                                         'Mobile Safari/537.36'}


def counter(url: str) -> int:
    full_url = f'{PRE_URL}/{url}'
    req = requests.get(full_url, HEADERS).content
    soup = bs(req, 'html.parser')
    try:
        count = soup.find('button', class_='Button Button_color_blue Button_size_m Button_type_button Button_width_full')
        get_info_ON_button = str(count).split('Показать ')[1]
        numb = re.sub('\D', '', get_info_ON_button)
    except AttributeError:
        numb = 0
    return int(numb)


def message(text: str) -> None:
    URL = (
        'https://api.telegram.org/bot{token}/sendMessage'.format(token=TLG_TOKEN))
    data = {'chat_id': CHAT,
            'text': text
            }
    requests.post(URL, data=data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        time_now = datetime.now()# + datetime.timedelta(hours=3)
        h = time_now.hour
        count = 0
        if h in range(9, 21):
            for url in URLS:
                count += counter(url)
            if count < 500:
                text = f'База опустилась до:\n{count} объявлений'
                message(text)
            elif h == 14:
                text = f'Текущий сток:\n{count} объявлений'
                print(text)
                message(text)
            sleep(3600)
        else:
            sleep(46000)
