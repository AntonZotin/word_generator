from src.eda.radio_window import get_radio_eda, radio_eda
from src.utils.checklist_strings import eda_docs, eda_docs_mapping, fizik
from src.utils.strings import EDA_2_WINDOW


radios = {}


def get_eda_2_window(data={'type': fizik}):
    global radios
    radios = {}
    index = 1
    for c, perm, maybe in eda_docs:
        if not c.startswith('HEADER ') and data['type'] in perm:
            c = c.replace('\\n', '\n')
            radios[str(index)] = c
            index += 1
    return get_radio_eda(data, eda_docs, EDA_2_WINDOW)


def eda_2_event(window, event, values, data):
    return radio_eda(window, event, values, radios, eda_docs_mapping, 'error_docs')
