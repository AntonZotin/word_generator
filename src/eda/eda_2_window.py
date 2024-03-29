from src.utils.checklist_strings import eda_docs
from src.utils.decorators import exception_handler
from src.eda.eda_3_window import eda_3
from src.utils.radio_window import radio_eda
from src.utils.strings import EDA_2_WINDOW


@exception_handler
def eda_2(data):
    return radio_eda(data, eda_docs, EDA_2_WINDOW, 'error_docs', eda_3)
