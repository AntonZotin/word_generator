import requests
from requests.auth import HTTPProxyAuth


def search_by_inn(inn, login, password):
    auth = HTTPProxyAuth(login, password)
    proxy = {
        'http': 'http://i.tatar.ru:8080',
        'https': 'http://i.tatar.ru:8080'
    }
    res = requests.post("https://egrul.nalog.ru/", proxies=proxy, auth=auth, data={"query": inn}).json()
    code = res['t']
    res2 = requests.get(f'https://egrul.nalog.ru/search-result/{code}', proxies=proxy, auth=auth).json().get('rows', [])
    return res2[0] if len(res2) else {}
