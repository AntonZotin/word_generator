import traceback

import PySimpleGUI as Gui

first_button = 'Доставка'
second_button = 'Процентная ставка'


def main(program, customer):
    layout = [
        [
            Gui.Frame('Labelled Group', [[
                Gui.Submit(button_text=first_button, size=(12, 6)),
                Gui.Submit(button_text=second_button, size=(12, 6))
            ]])
        ]
    ]
    window = Gui.Window('Выбор заявителя', layout, grab_anywhere=False, size=(300, 120)).Finalize()

    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit', 'Cancel', 'Закрыть'):
            return 0
        elif event == first_button or event == second_button:
            window.hide()
            # sec_main(program, event)
            window.un_hide()


def run(program, customer):
    try:
        main(program, customer)
    except Exception as e:
        Gui.PopupAnimated(None)
        tb = traceback.format_exc()
        Gui.popup_error(f'An error happened. Here is the info:', e, tb)
