import re

import requests
from requests.auth import HTTPProxyAuth


def search_by_inn(inn, need_proxy):
    if need_proxy:
        auth_url = f'http://Govtatar%5CElena.Zotina:12345qwerty@i.tatar.ru:8080'
        s = requests.Session()
        s.proxies = {
            "http": auth_url,
            "https": auth_url
        }
        s.auth = HTTPProxyAuth('Govtatar\\Elena.Zotina', '12345qwerty')
        s.trust_env = False
        res = s.post("https://egrul.nalog.ru/", data={"query": inn}).json()
        code = res['t']
        res2 = s.get(f'https://egrul.nalog.ru/search-result/{code}').json().get('rows', [])
        return res2[0] if len(res2) else {}
    else:
        res = requests.post("https://egrul.nalog.ru/", data={"query": inn}).json()
        code = res['t']
        res2 = requests.get(f'https://egrul.nalog.ru/search-result/{code}').json().get('rows', [])
        return res2[0] if len(res2) else {}


def extract_radio_values(values, radios):
    grouped = {}
    for k, v in values.items():
        matched = re.match('RADIO(\d+)-(\w+)', k)
        if matched:
            index, name = matched.groups()
            if index in grouped:
                grouped[index][name] = v
            else:
                grouped[index] = {name: v}
        matched = re.match('TEXT(\d+)', k)
        if v and matched:
            index = matched.groups()[0]
            if index in grouped:
                grouped[index]['text'] = v
            else:
                grouped[index] = {'text': v}
    result = []
    for gid, g in grouped.items():
        if 'text' in g:
            result.append(g["text"])
        elif list(g.values()) == [False, False]:
            result.append(radios[gid])
        elif g.get('no'):
            result.append(radios[gid])
    return result


def filter_key(name):
    matched = re.match('RADIO(\d+)-(\w+)', name).groups()
    return matched[0] if matched[1] == 'no' else None


def separate_comment(comment):
    return [re.sub('^\d+[.)\s+]+', '', c) for c in comment.strip().split('\n')]
