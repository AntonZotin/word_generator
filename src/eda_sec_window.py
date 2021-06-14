import traceback

import PySimpleGUI as Gui

from src.checklist_strings import fizik, yurik
from src.eda_third_window import run as eda_thi_main

required_fields = {
    'name': 'Наименование компании',
    'inn': 'ИНН',
    'number': 'Номер заявки',
    'date': 'Дата заявки',
}

numeric_fields = ['inn', 'number']


def main():
    layout = [
        [Gui.Text('Наименование компании', size=(20, 1)), Gui.InputText(size=(42, 1), key='name')],
        [Gui.Text('ИНН', size=(20, 1)), Gui.Input(size=(42, 1), key='inn', enable_events=True)],
        [Gui.Text('Номер заявки', size=(20, 1)), Gui.Input(size=(42, 1), key='number', enable_events=True)],
        [Gui.Text('Дата заявки', size=(20, 1)), Gui.Input(size=(42, 1), key='date', enable_events=True)],
        [Gui.Text('Тип заявителя', size=(20, 1)),
         Gui.Radio(fizik, default=True, group_id='1', key=fizik),
         Gui.Radio(yurik, default=False, group_id='1', key=yurik), Gui.Text('', size=(5, 1))],
        [Gui.Submit(button_text='Далее'), Gui.Submit(button_text='Назад')]
    ]
    Gui.PopupAnimated(None)
    window = Gui.Window('Выбор программы', layout, grab_anywhere=False, size=(400, 170),
                        element_justification='c').Finalize()

    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit', 'Cancel', 'Закрыть'):
            return 0
        elif event == 'Назад':
            window.close()
            break
        elif event in numeric_fields and values[event] and values[event][-1] not in '0123456789':
            window[event].update(values[event][:-1])
        elif event == 'date' and values[event]:
            if len(values[event]) == 2 or len(values[event]) == 5:
                window[event].update(values[event] + '.')
            elif len(values[event]) == 11:
                window[event].update(values[event][:-1])
        elif event == 'Далее':
            result = {
                'name': values['name'],
                'inn': values['inn'],
                'number': values['number'],
                'date': values['date'],
                'type': fizik if values[fizik] is True else yurik
            }
            required_errors = []
            if not values['name']: required_errors.append(required_fields['name'])
            if not values['inn']: required_errors.append(required_fields['inn'])
            if not values['number']: required_errors.append(required_fields['number'])
            if not values['date']: required_errors.append(required_fields['date'])

            if not required_errors:
                # window['name'].update('')
                # window['inn'].update('')
                # window['number'].update('')
                # window['date'].update('')
                window.hide()
                eda_thi_main(result)
                window.un_hide()
            else:
                Gui.popup('Вы не ввели обязательные поля:\n%s' % ', '.join(required_errors), title='Пустые поля')


def run():
    try:
        main()
    except Exception as e:
        Gui.PopupAnimated(None)
        tb = traceback.format_exc()
        Gui.popup_error(f'An error happened. Here is the info:', e, tb)
