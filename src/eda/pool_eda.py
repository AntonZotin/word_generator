import PySimpleGUI as sg

from src.eda.eda_1_window import get_eda_1_window, eda_1_event
from src.eda.eda_2_window import get_eda_2_window, eda_2_event
from src.eda.eda_3_window import get_eda_3_window, eda_3_event
from src.eda.eda_4_window import get_eda_4_window, eda_4_event
from src.eda.eda_5_window import get_eda_5_window, eda_5_event
from src.eda.template_window import get_template_window, template_event
from src.utils.decorators import exception_handler
from src.utils.strings import EDA_1_WINDOW, TEMPLATE_WINDOW, EDA_2_WINDOW, EDA_3_WINDOW, EDA_4_WINDOW, EDA_5_WINDOW, \
    COMMENTS_FILE, END_OF_COMMENT, SUCCESS, CLEAR

names = [
    EDA_1_WINDOW,
    EDA_2_WINDOW,
    EDA_3_WINDOW,
    EDA_4_WINDOW,
    EDA_5_WINDOW
]
create_window_pool = {
    EDA_1_WINDOW: get_eda_1_window,
    EDA_2_WINDOW: get_eda_2_window,
    EDA_3_WINDOW: get_eda_3_window,
    EDA_4_WINDOW: get_eda_4_window,
    EDA_5_WINDOW: get_eda_5_window,
    TEMPLATE_WINDOW: get_template_window
}
event_window_pool = {
    EDA_1_WINDOW: eda_1_event,
    EDA_2_WINDOW: eda_2_event,
    EDA_3_WINDOW: eda_3_event,
    EDA_4_WINDOW: eda_4_event,
    EDA_5_WINDOW: eda_5_event,
    TEMPLATE_WINDOW: template_event
}


def get_previous_window(name):
    index = names.index(name)
    new_index = index - 1
    return names[new_index]


def get_next_window(name):
    index = names.index(name)
    new_index = index + 1
    return names[new_index]


def init_windows():
    return {
        EDA_1_WINDOW: get_eda_1_window(),
        EDA_2_WINDOW: None,
        EDA_3_WINDOW: None,
        EDA_4_WINDOW: None,
        EDA_5_WINDOW: None,
        TEMPLATE_WINDOW: None
    }


def clear(window_pool):
    for w in window_pool.values():
        if w:
            w.close()
    return {}, init_windows()


@exception_handler
def pool_eda():
    window_pool = init_windows()
    result = {}
    while True:
        window, event, values = sg.read_all_windows()
        if window:
            window_title = window.Title
            if event in (None, 'Exit', 'Cancel', 'Закрыть'):
                return 0
            elif event == 'Сбросить все':
                result, window_pool = clear(window_pool)
            elif event == 'Назад':
                window.hide()
                prev_window = window_pool[get_previous_window(window_title)]
                prev_window.un_hide()
            elif event == 'Далее':
                status, res = event_window_pool[window_title](window, event, values, result)
                if status == SUCCESS:
                    result.update(res)
                    window.hide()
                    next_name = get_next_window(window_title)
                    next_window = window_pool[next_name]
                    if next_window:
                        next_window.un_hide()
                    else:
                        window_pool[next_name] = create_window_pool[next_name](result)
            elif event == 'Confirm':
                window.close()
            elif event.startswith('TEMPLATE'):
                with open(COMMENTS_FILE, 'r+') as t:
                    comments_file = t.read().strip()
                    comments_array = set(e.strip() for e in filter(lambda el: el, comments_file.split(
                        END_OF_COMMENT))) if comments_file else set()
                get_template_window(comments_array, event, window, values)
            else:
                status = event_window_pool[window_title](window, event, values, result)
                if status == CLEAR:
                    result, window_pool = clear(window_pool)
