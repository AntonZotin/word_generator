import traceback

import PySimpleGUI as Gui

from src.eda_third_window import run as eda_thi_main


required_fields = {
    'name': 'Наименование компании',
    'inn': 'ИНН',
    'number': 'Номер заявки',
    'date': 'Дата заявки',
}

numeric_fields = ['inn', 'number']

fizik = 'Физ.лицо'
yurik = 'Юр.лицо'


def main():
    layout = [
        [Gui.Text('Наименование компании', size=(20, 1)), Gui.InputText(size=(42, 1), key='name')],
        [Gui.Text('ИНН', size=(20, 1)), Gui.Input(size=(42, 1), key='inn', enable_events=True)],
        [Gui.Text('Номер заявки', size=(20, 1)), Gui.Input(size=(42, 1), key='number', enable_events=True)],
        [Gui.Text('Дата заявки', size=(20, 1)), Gui.Input(size=(42, 1), key='date', enable_events=True)],
        [Gui.Text('Тип заявителя', size=(20, 1)),
         Gui.Radio(fizik, default=True, group_id='1', key=fizik),
         Gui.Radio(yurik, default=False, group_id='1', key=yurik)],
        [Gui.Submit(button_text='Далее'), Gui.Submit(button_text='Назад')]
    ]
    Gui.PopupAnimated(None)
    window = Gui.Window('Выбор программы', layout, grab_anywhere=False, size=(300, 120), element_justification='c').Finalize()

    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit', 'Cancel', 'Закрыть'):
            return 0
        elif event in numeric_fields and values[event] and values[event][-1] not in '0123456789':
            window[event].update(values[event][:-1])
        elif event == 'date' and values[event]:
            if len(values[event]) == 2 or len(values[event]) == 5:
                window[event].update(values[event] + '.')
            elif len(values[event]) == 11:
                window[event].update(values[event][:-1])
        elif event == 'Далее':
            required_errors = []
            name = values['name']
            window['name'].update('')
            if not name: required_errors.append(required_fields['name'])
            inn = values['inn']
            window['inn'].update('')
            if not inn: required_errors.append(required_fields['inn'])
            number = values['number']
            window['number'].update('')
            if not number: required_errors.append(required_fields['number'])
            date = values['date']
            window['date'].update('')
            if not date: required_errors.append(required_fields['date'])

            if not required_errors:
                window.hide()
                eda_thi_main()
                window.un_hide()


def run():
    try:
        main()
    except Exception as e:
        Gui.PopupAnimated(None)
        tb = traceback.format_exc()
        Gui.popup_error(f'An error happened. Here is the info:', e, tb)
