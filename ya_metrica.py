from pprint import pprint
from urllib.parse import urlencode

import requests

APP_ID = '66424858b19f4059896f4d1fcf31aab0'
AUTH_URL = 'https://oauth.yandex.ru/authorize'

data = {
    'response_type': 'token',
    'client_id': APP_ID
}

# print('?'.join((AUTH_URL, urlencode(data))))

token = 'AQAAAAAZnGNWAATJoZ5i-WHmmUIap-C0hZ9cIlg'


class YaMetrikaMain:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Authorization': 'OAuth {}'.format(self.token)
        }


class YaMetrikaUser(YaMetrikaMain):
    def get_counters(self):

        response = requests.get('https://api-metrika.yandex.ru/management/v1/counters', headers=self.get_headers())

        return [c['id'] for c in response.json()['counters']]


class YaMetrikaCounter(YaMetrikaMain):
    def __init__(self, token, counter_id):
        self.counter_id = counter_id
        super().__init__(token)

    def get_info(self):
        response = requests.get('https://api-metrika.yandex.ru/management/v1/counter/{}'.format(self.counter_id),
                                headers=self.get_headers())
        return response.json()

    def get_visits(self):
        params = {
            'id': self.counter_id,
            'metrics': 'ym:s:visits'
        }
        response = requests.get('https://api-metrika.yandex.ru/stat/v1/data', params, headers=self.get_headers())

        return response.json()['data'][0]['metrics']

    def get_page_views(self):
        params = {
            'id': self.counter_id,
            'metrics': 'ym:s:pageviews'
        }
        response = requests.get('https://api-metrika.yandex.ru/stat/v1/data', params, headers=self.get_headers())

        return response.json()['data'][0]['metrics']

    def get_users(self):
        params = {
            'id': self.counter_id,
            'metrics': 'ym:s:users'
        }
        response = requests.get('https://api-metrika.yandex.ru/stat/v1/data', params, headers=self.get_headers())

        return response.json()['data'][0]['metrics']


ya_user_1 = YaMetrikaUser(token)


def get_data():

    print('Введите команду для получения статистики: 1 - визиты, 2 - просмотры, 3 - посетители')
    command = int(input())

    for counter_id in ya_user_1.get_counters():
        counter = YaMetrikaCounter(token, counter_id)

        if command == 1:
            i = counter.get_visits()
            print(i)

        elif command == 2:
            i = counter.get_page_views()
            print(i)

        elif command == 3:
            i = counter.get_users()
            print(i)


get_data()

