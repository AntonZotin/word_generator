import traceback

import PySimpleGUI as Gui

from src.images import splash
from src.second_window import run as sec_main


first_button = 'Доставка'
second_button = 'Процентная\nставка'


def main():
    Gui.PopupAnimated(splash)
    layout = [
        [Gui.Submit(button_text=first_button, size=(12, 6)),
         Gui.Submit(button_text=second_button, size=(12, 6))]
    ]
    Gui.PopupAnimated(None)
    window = Gui.Window('Выбор программы', layout, grab_anywhere=False, size=(300, 120), element_justification='c').Finalize()

    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit', 'Cancel', 'Закрыть'):
            return 0
        elif event == first_button or event == second_button:
            window.hide()
            sec_main(event)
            window.un_hide()


def run():
    try:
        main()
    except Exception as e:
        Gui.PopupAnimated(None)
        tb = traceback.format_exc()
        Gui.popup_error(f'An error happened. Here is the info:', e, tb)
