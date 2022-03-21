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


def extract_radio_values(values, radios, radios_mapping):
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
        elif (list(g.values()) == [False, False] and 'maybe' not in g) or g.get('no'):
            row = radios_mapping[radios[gid]] if radios[gid] in radios_mapping else radios[gid]
            result.append(row)
    return result


def filter_key(name):
    matched = re.match('RADIO(\d+)-(\w+)', name).groups()
    return matched[0] if matched[1] == 'no' else None


def separate_comment(comment):
    return [re.sub('^\d+[.)\s+]+', '', c) for c in comment.strip().split('\n')]


def find_in_comments(comment, comments_array):
    for ca in comments_array:
        pattern = re.compile(ca.replace('/', '|').replace('--', '\d+'))
        if re.match(pattern, comment):
            return True
    return False


def onKeyRelease(event):
    ctrl = (event.state & 0x4) != 0
    if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
        event.widget.event_generate("<<Cut>>")

    if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")

    if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")
