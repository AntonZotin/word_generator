import requests


def search_by_inn(inn):
    res = requests.post("https://egrul.nalog.ru/", data={"query": inn}).json()
    code = res['t']
    res2 = requests.get(f'https://egrul.nalog.ru/search-result/{code}').json().get('rows', [])
    return res2[0] if len(res2) else {}
