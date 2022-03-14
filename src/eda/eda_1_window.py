import traceback
from datetime import datetime

import PySimpleGUI as Gui
from urllib3.exceptions import SSLError

from src.checklist_strings import fizik, yurik
from src.eda.eda_2_window import run as eda_2
from src.strings import specialists
from src.utils import search_by_inn

required_fields = {
    'name': 'Наименование компании',
    'inn': 'ИНН',
    'number': 'Номер заявки',
    'request_date': 'Дата заявки',
    'ispolnitel': 'Исполнитель',
    'check_date': 'Дата проверки',
}

numeric_fields = ['inn', 'number']


def insert_name(inn, prefix, window):
    try:
        name = search_by_inn(inn).get('n')
    except SSLError:
        name = search_by_inn(inn, 'http').get('n')
    if name is not None:
        window['name'].update(f"{prefix}{name}")
    else:
        Gui.popup('Данные от ЕГРЮЛ отсутствуют.', title='Пустые поля')


def main():
    now = datetime.now()
    string_now = now.strftime('%d.%m.%Y')
    layout = [
        [Gui.Text('Тип заявителя', size=(20, 1)),
         Gui.Radio(fizik, default=True, group_id='1', key=fizik),
         Gui.Radio(yurik, default=False, group_id='1', key=yurik), Gui.Text('', size=(5, 1))],
        [Gui.Text('ИНН', size=(20, 1)), Gui.Input(size=(42, 1), key='inn', enable_events=True)],
        [Gui.Text('Наименование компании', size=(20, 1)), Gui.InputText(size=(42, 1), key='name')],
        [Gui.Text('Дата заявки', size=(20, 1)), Gui.Input(size=(16, 1), key='request_date', enable_events=True),
         Gui.CalendarButton('Календарь',  target='request_date', default_date_m_d_y=(now.month, now.day, now.year),
                            format="%d.%m.%Y")],
        [Gui.Text('Номер заявки', size=(20, 1)), Gui.Input(size=(42, 1), key='number', enable_events=True)],
        [Gui.Text('Исполнитель', size=(20, 1)), Gui.Combo([*specialists.keys()], size=(40, 1),
                                                          readonly=True, key='ispolnitel')],
        [Gui.Text('Дата проверки', size=(20, 1)), Gui.Input(size=(16, 1), key='check_date', enable_events=True,
                                                            default_text=string_now),
         Gui.CalendarButton('Календарь',  target='check_date', default_date_m_d_y=(now.month, now.day, now.year),
                            format="%d.%m.%Y")],
        [Gui.Submit(button_text='Далее')]
    ]
    Gui.PopupAnimated(None)
    window = Gui.Window('Общие данные', layout, grab_anywhere=False, size=(400, 240),
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
        elif event == 'inn' and values[event]:
            if len(values[event]) == 10 and values[yurik]:
                insert_name(values[event], '', window)
            elif len(values[event]) == 12 and values[fizik]:
                insert_name(values[event], 'ИП ', window)
        elif (event == 'request_date' or event == 'check_date') and values[event]:
            if len(values[event]) == 2 or len(values[event]) == 5:
                window[event].update(values[event] + '.')
            elif len(values[event]) == 11:
                window[event].update(values[event][:-1])
            window['number'].update(values[event].replace('.', ''))
        elif event == 'Далее':
            result = {
                'name': values['name'],
                'inn': values['inn'],
                'number': values['number'],
                'request_date': values['request_date'],
                'type': fizik if values[fizik] is True else yurik,
                'ispolnitel': values['ispolnitel'],
                'check_date': values['check_date'],
            }
            required_errors = []
            if not values['inn']: required_errors.append(required_fields['inn'])
            if not values['name']: required_errors.append(required_fields['name'])
            if not values['number']: required_errors.append(required_fields['number'])
            if not values['request_date']: required_errors.append(required_fields['request_date'])
            if not values['ispolnitel']: required_errors.append(required_fields['ispolnitel'])
            if not values['check_date']: required_errors.append(required_fields['check_date'])

            if not required_errors:
                window.hide()
                res = eda_2(result)
                if res == 'back':
                    window[fizik].update(True)
                    window[yurik].update(False)
                    window['inn'].update('')
                    window['name'].update('')
                    window['number'].update('')
                    window['request_date'].update('')
                    window['ispolnitel'].update('')
                    window['check_date'].update('')
                elif res == 0:
                    return 0
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
        return 0
