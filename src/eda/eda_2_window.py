import re
import traceback

import PySimpleGUI as Gui

from src.checklist_strings import eda_docs, header_max_symbols, text_max_symbols
from src.eda.eda_3_window import run as eda_3
from src.eda.comment_modal import run as comment


def filter_key(name):
    matched = re.match('RADIO(\d+)-(\w+)', name).groups()
    return matched[0] if matched[1] == 'no' else None


def main(data):
    arr = []
    radios = {}
    index = 1
    for c, perm, maybe in eda_docs:
        if c.startswith('HEADER '):
            c = c.replace('HEADER ', '')
            arr += [
                [Gui.Text(c, size=(66, int(len(c) / header_max_symbols)), justification='center',
                          font=("Helvetica", 18), relief=Gui.RELIEF_RIDGE)],
                [Gui.Text('-' * 230)]
            ]
        elif data['type'] in perm:
            c = c.replace('\\n', '\n')
            height = int(len(c) / text_max_symbols)
            height += int(c.count('\n') / 5)
            predstav = 'для представителя' in c
            width = 69 if predstav else 85
            prefix_arr = [Gui.Text(c, size=(width, height), key=f"RADIO{index}-text"), ]
            if predstav:
                prefix_arr.append(Gui.Radio('Сам заявитель', f"RADIO{index}", key=f"RADIO{index}-yeah",
                                            enable_events=True))
            arr += [
                [*prefix_arr, Gui.VerticalSeparator(),
                 Gui.Radio('да', f"RADIO{index}", key=f"RADIO{index}-yes", enable_events=True),
                 Gui.Radio('нет', f"RADIO{index}", key=f"RADIO{index}-{'maybe' if maybe else 'no'}", enable_events=True),
                 Gui.Submit(button_text='Комментарий', key=f"BUTTON{index}")],
                [Gui.Text('-' * 230)]
            ]
            radios[str(index)] = c
            index += 1

    layout = [
        [Gui.Col(arr, size=(950, 780), scrollable=True, vertical_scroll_only=True)],
        [Gui.Submit(button_text='Далее'), Gui.Submit(button_text='Назад'), Gui.Submit(button_text='Сбросить все')]
    ]
    window = Gui.Window('Документы обязательные для предоставления', layout, grab_anywhere=False,
                        element_justification='c').Finalize()

    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit', 'Cancel', 'Закрыть'):
            return 0
        elif event == 'Сбросить все':
            window.close()
            return 'back'
        elif 'RADIO' in str(event):
            res = event.replace('RADIO', '').split('-')
            if res[1] == 'yes' or res[1] == 'yeah':
                window[f"RADIO{res[0]}-text"].update(text_color='#37ff5a')
            elif res[1] == 'maybe':
                window[f"RADIO{res[0]}-text"].update(text_color='#ffa500')
            else:
                window[f"RADIO{res[0]}-text"].update(text_color='#ff4f4f')
        elif 'BUTTON' in str(event):
            index = event.replace('BUTTON', '')
            window.hide()
            res = comment()
            if res == 'back':
                return 'back'
            elif res == 0:
                return 0
            window.un_hide()
            if res:
                window[f"RADIO{index}-text"].update(value=res)
        elif event == 'Назад':
            window.close()
            break
        elif event == 'Далее':
            filtered = [filter_key(k) for k, v in values.items() if v is True]
            data['error_docs'] = [radios[f] for f in filtered if f is not None]
            window.hide()
            res = eda_3(data)
            if res == 'back':
                return 'back'
            elif res == 0:
                return 0
            window.un_hide()


def run(data):
    try:
        return main(data)
    except Exception as e:
        Gui.PopupAnimated(None)
        tb = traceback.format_exc()
        Gui.popup_error(f'An error happened. Here is the info:', e, tb)
        return 0
