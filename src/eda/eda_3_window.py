from src.eda.radio_window import get_radio_eda, radio_eda
from src.utils.checklist_strings import eda_crits, eda_crits_mapping
from src.utils.strings import EDA_3_WINDOW


radios = {}


def get_eda_3_window(data):
    global radios
    radios = {}
    index = 1
    for c, perm, maybe in eda_crits:
        if not c.startswith('HEADER ') and data['type'] in perm:
            c = c.replace('\\n', '\n')
            radios[str(index)] = c
            index += 1
    return get_radio_eda(data, eda_crits, EDA_3_WINDOW)


def eda_3_event(window, event, values, data):
    return radio_eda(window, event, values, radios, eda_crits_mapping, 'error_crits')
