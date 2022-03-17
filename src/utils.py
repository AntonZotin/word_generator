import re

import requests
from requests.auth import HTTPProxyAuth


def search_by_inn(inn, host, login, password):
    auth = HTTPProxyAuth(login, password)
    proxy = {
        'http': host,
        'https': host
    }
    res = requests.post("https://egrul.nalog.ru/", proxies=proxy, auth=auth, data={"query": inn}).json()
    code = res['t']
    res2 = requests.get(f'https://egrul.nalog.ru/search-result/{code}', proxies=proxy, auth=auth).json().get('rows', [])
    return res2[0] if len(res2) else {}


def check_proxy(host, login, password):
    auth = HTTPProxyAuth(login, password)
    proxy = {
        'http': host,
        'https': host
    }
    res = requests.get("https://www.mulesoft.com/pw/prod/oneTrustv2/consent/04856e97-6bf2-42aa-9a14-8122a16ebcf2"
                       "/9271b9d0-7992-4364-9721-eac93d9415b0/en.json",
                       proxies=proxy, auth=auth)
    if res.status_code == 200:
        return res.json(), 200
    else:
        return str(res.content), res.status_code


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
            result.append(f'{radios[gid]} ({g["text"]})')
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
