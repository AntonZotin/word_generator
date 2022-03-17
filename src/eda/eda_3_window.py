from src.utils.checklist_strings import eda_crits
from src.utils.decorators import exception_handler
from src.eda.eda_4_window import eda_4
from src.utils.radio_window import radio_eda
from src.utils.strings import EDA_3_WINDOW


@exception_handler
def eda_3(data):
    return radio_eda(data, eda_crits, EDA_3_WINDOW, 'error_crits', eda_4)
