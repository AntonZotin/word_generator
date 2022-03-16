import traceback

import PySimpleGUI as Gui

from src.eda.eda_1_window import run as eda_1

required_fields = {
    'login': 'Логин',
    'password': 'Пароль',
}


def main():
    layout = [
        [Gui.Text('Логин', size=(5, 1)), Gui.InputText(size=(42, 1), key='login')],
        [Gui.Text('Пароль', size=(5, 1)), Gui.InputText(size=(42, 1), key='password')],
        [Gui.Submit(button_text='Далее')]
    ]
    Gui.PopupAnimated(None)
    window = Gui.Window('Доступ к прокси', layout, grab_anywhere=False, size=(300, 100),
                        element_justification='c').Finalize()

    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit', 'Cancel', 'Закрыть'):
            return 0
        elif event == 'Назад':
            window.close()
            break
        elif event == 'Далее':
            result = {
                'login': values['login'],
                'password': values['password']
            }
            required_errors = []
            if not values['login']: required_errors.append(required_fields['login'])
            if not values['password']: required_errors.append(required_fields['password'])

            if not required_errors:
                window.hide()
                res = eda_1(result)
                if res == 'back':
                    window['login'].update('')
                    window['password'].update('')
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
