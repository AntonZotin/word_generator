import requests


def search_by_inn(inn, proto='https'):
    res = requests.post(f"{proto}://egrul.nalog.ru/", data={"query": inn}).json()
    code = res['t']
    res2 = requests.get(f'{proto}://egrul.nalog.ru/search-result/{code}').json().get('rows', [])
    return res2[0] if len(res2) else {}
