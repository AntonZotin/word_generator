import traceback

import PySimpleGUI as Gui

from src.checklist_strings import strings

header_max_symbols = 50
text_max_symbols = 80


def main(program, customer):
    arr = []
    index = 1
    for c in strings:
        if c.startswith('HEADER '):
            c = c.replace('HEADER ', '')
            arr += [
                [Gui.Text(c, size=(66, int(len(c) / header_max_symbols)), justification='center',
                          font=("Helvetica", 18), relief=Gui.RELIEF_RIDGE)],
                [Gui.Text('-' * 230)]
            ]
        else:
            c = c.replace('\\n', '\n')
            height = int(len(c) / text_max_symbols)
            height += int(c.count('\n') / 5)
            arr += [
                [Gui.Text(c, size=(100, height), key=f"RADIO{index}-text"), Gui.VerticalSeparator(),
                 Gui.Radio('да', f"RADIO{index}", key=f"RADIO{index}-yes", enable_events=True),
                 Gui.Radio('нет', f"RADIO{index}", key=f"RADIO{index}-no", enable_events=True)],
                [Gui.Text('-' * 230)]
            ]
            index += 1

    layout = [
        [Gui.Col(arr, size=(950, 780), scrollable=True, vertical_scroll_only=True)],
        [Gui.Submit(button_text='Результат', key='Result')],
        [Gui.Submit(button_text='Назад')]
    ]
    window = Gui.Window('Документы обязательные для предоставления', layout, grab_anywhere=False,
                        element_justification='c').Finalize()

    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit', 'Cancel', 'Закрыть'):
            return 0
        elif 'RADIO' in str(event):
            res = event.replace('RADIO', '').split('-')
            if res[1] == 'yes':
                window[f"RADIO{res[0]}-text"].update(text_color='#37ff5a')
            else:
                window[f"RADIO{res[0]}-text"].update(text_color='#ff4f4f')
        elif event == 'Назад':
            window.close()
            break


def run(program, customer):
    try:
        main(program, customer)
    except Exception as e:
        Gui.PopupAnimated(None)
        tb = traceback.format_exc()
        Gui.popup_error(f'An error happened. Here is the info:', e, tb)
