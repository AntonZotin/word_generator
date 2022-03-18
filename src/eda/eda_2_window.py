from src.eda.radio_window import get_radio_eda, radio_eda
from src.utils.checklist_strings import eda_docs
from src.utils.strings import EDA_2_WINDOW


def get_eda_2_window(zayavitel_type):
    return get_radio_eda(zayavitel_type, eda_docs, EDA_2_WINDOW)


def eda_2_event(window, event, values, radios):
    return radio_eda(window, event, values, radios)
