import traceback

import PySimpleGUI as Gui
from src.third_window import run as thi_main

one_first_button = 'Первая'
one_second_button = 'Вторая'
one_third_button = 'Третья'

two_first_button = 'Первая'
two_second_button = 'Вторая'
two_third_button = 'Третья'


def main(program):
    layout = [
        [
            Gui.Frame('I категория', [[
                Gui.Submit(button_text=one_first_button, size=(12, 6)),
                Gui.Submit(button_text=one_second_button, size=(12, 6)),
                Gui.Submit(button_text=one_third_button, size=(12, 6))
            ]], pad=(10, 10))
        ],
        [
            Gui.Frame('II категория', [[
                Gui.Submit(button_text=two_first_button, size=(12, 6)),
                Gui.Submit(button_text=two_second_button, size=(12, 6)),
                Gui.Submit(button_text=two_third_button, size=(12, 6))
            ]], pad=(10, 10))
        ],
        [Gui.Text('', size=(25, 1)), Gui.Submit(button_text='Назад')]
    ]
    window = Gui.Window('Выбор заявителя', layout, grab_anywhere=False, size=(370, 400)).Finalize()

    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit', 'Cancel', 'Закрыть'):
            return 0
        elif event in (one_first_button, one_second_button, one_third_button,
                       two_first_button, two_second_button, two_third_button):
            window.hide()
            thi_main(program, event)
            window.un_hide()
        elif event == 'Назад':
            window.close()
            break


def run(program):
    try:
        main(program)
    except Exception as e:
        Gui.PopupAnimated(None)
        tb = traceback.format_exc()
        Gui.popup_error(f'An error happened. Here is the info:', e, tb)
