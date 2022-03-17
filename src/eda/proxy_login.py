import PySimpleGUI as Gui

from src.eda.decorators import exception_handler
from src.eda.eda_1_window import eda_1
from src.utils import check_proxy

required_fields = {
    'host': 'Хост',
    'login': 'Логин',
    'password': 'Пароль',
}


@exception_handler
def proxy_window():
    layout = [
        [Gui.Text('Хост', size=(5, 1)), Gui.InputText(size=(42, 1), key='host', default_text='http://i.tatar.ru:8080')],
        [Gui.Text('Логин', size=(5, 1)), Gui.InputText(size=(42, 1), key='login')],
        [Gui.Text('Пароль', size=(5, 1)), Gui.InputText(size=(42, 1), key='password')],
        [Gui.Submit(button_text='Далее'), Gui.Submit(button_text='Проверить')]
    ]
    Gui.PopupAnimated(None)
    window = Gui.Window('Доступ к прокси', layout, grab_anywhere=False, size=(300, 120),
                        element_justification='c').Finalize()

    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit', 'Cancel', 'Закрыть'):
            return 0
        elif event == 'Назад':
            window.close()
            break
        elif event == 'Проверить':
            res, status = check_proxy(values['host'], values['login'], values['password'])
            Gui.popup(res, title=f'Статус {status}')
        elif event == 'Далее':
            result = {
                'host': values['host'],
                'login': values['login'],
                'password': values['password']
            }
            required_errors = []
            if not values['host']: required_errors.append(required_fields['host'])
            if not values['login']: required_errors.append(required_fields['login'])
            if not values['password']: required_errors.append(required_fields['password'])

            if not required_errors:
                window.hide()
                res = eda_1(result)
                if res == 'back':
                    window['host'].update('')
                    window['login'].update('')
                    window['password'].update('')
                elif res == 0:
                    return 0
                window.un_hide()
            else:
                Gui.popup('Вы не ввели обязательные поля:\n%s' % ', '.join(required_errors), title='Пустые поля')
