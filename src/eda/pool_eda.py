import PySimpleGUI as sg

from src.eda.eda_1_window import get_eda_1_window, eda_1_event
from src.eda.eda_2_window import get_eda_2_window, eda_2_event
from src.eda.eda_3_window import get_eda_3_window, eda_3_event
from src.eda.eda_4_window import get_eda_4_window, eda_4_event
from src.eda.eda_5_window import get_eda_5_window, eda_5_event
from src.eda.template_window import get_template_window, template_event
from src.utils.decorators import exception_handler
from src.utils.strings import EDA_1_WINDOW, TEMPLATE_WINDOW, EDA_2_WINDOW, EDA_3_WINDOW, EDA_4_WINDOW, EDA_5_WINDOW, \
    COMMENTS_FILE, END_OF_COMMENT, SUCCESS

window1, window2, window3, window4, window5, window_template = None, None, None, None, None, None


def get_previous_window(name):
    names = [EDA_1_WINDOW,
             EDA_2_WINDOW,
             EDA_3_WINDOW,
             EDA_4_WINDOW,
             EDA_5_WINDOW]
    index = names.index(name)
    new_index = index - 1
    return names[new_index]


def get_next_window(name):
    names = [EDA_1_WINDOW,
             EDA_2_WINDOW,
             EDA_3_WINDOW,
             EDA_4_WINDOW,
             EDA_5_WINDOW]
    index = names.index(name)
    new_index = index + 1
    return names[new_index]


@exception_handler
def pool_eda():
    global window1, window2, window3, window4, window5, window_template
    window1 = get_eda_1_window()

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
    window_pool = {
        EDA_1_WINDOW: window1,
        EDA_2_WINDOW: window2,
        EDA_3_WINDOW: window3,
        EDA_4_WINDOW: window4,
        EDA_5_WINDOW: window5,
        TEMPLATE_WINDOW: window_template
    }
    window_array = [window1, window2, window3, window4, window5, window_template]

    while True:
        window, event, values = sg.read_all_windows()
        if window:
            window_title = window.Title
            if event in (None, 'Exit', 'Cancel', 'Закрыть'):
                return 0
            elif event == 'Сбросить все':
                for w in window_array:
                    if w:
                        w.close()
                window1, window2, window3, window4, window5, window_template = get_eda_1_window(), None, None, None, None, None
            elif event == 'Назад':
                window.hide()
                prev_window = window_pool[get_previous_window(window_title)]
                prev_window.un_hide()
            elif event == 'Далее':
                status, res = event_window_pool[window_title](window, event, values)
                if status == SUCCESS:
                    window.hide()
                    next_name = get_next_window(window_title)
                    next_window = window_pool[next_name]
                    if next_window:
                        next_window.un_hide()
                    else:
                        window_pool[next_window] = create_window_pool[next_window]()
            elif event == 'Confirm':
                window.close()
            elif event.startswith('TEMPLATE'):
                with open(COMMENTS_FILE, 'r+') as t:
                    comments_file = t.read().strip()
                    comments_array = set(e.strip() for e in filter(lambda el: el, comments_file.split(
                        END_OF_COMMENT))) if comments_file else set()
                window_template = get_template_window(comments_array, event)
            else:
                event_window_pool[window_title](window, event, values)
