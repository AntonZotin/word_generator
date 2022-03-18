from src.eda.radio_window import get_radio_eda, radio_eda
from src.utils.checklist_strings import eda_crits
from src.utils.strings import EDA_3_WINDOW


def get_eda_3_window(zayavitel_type):
    return get_radio_eda(zayavitel_type, eda_crits, EDA_3_WINDOW)


def eda_3_event(window, event, values, radios):
    return radio_eda(window, event, values, radios)
