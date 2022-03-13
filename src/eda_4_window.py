import traceback

import PySimpleGUI as Gui

from src.eda_5_window import run as eda_5


def main(data):
    yandex = [[Gui.Text('Яндекс еда')],
              [Gui.Multiline(size=(30, 10), key='yandex', disabled=False)]]

    delivery = [[Gui.Text('Деливери')],
              [Gui.Multiline(size=(30, 10), key='delivery', disabled=False)]]

    layout = [
        [Gui.Text('Сумма по заявлению', size=(20, 1)), Gui.InputText(size=(20, 1), key='summ')],
        [Gui.Text(' ' * 60)],
        [Gui.Column(yandex, element_justification='c'), Gui.VSeperator(),
         Gui.Column(delivery, element_justification='c')],
        [Gui.Text(' ' * 60)],
        [Gui.Submit(button_text='Далее'), Gui.Submit(button_text='Назад'), Gui.Submit(button_text='В начало')]
    ]
    window = Gui.Window('Сумма понесенных затрат', layout, grab_anywhere=False,
                        element_justification='c').Finalize()

    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit', 'Cancel', 'Закрыть'):
            return 0
        elif event == 'В начало':
            window.close()
            return 'back'
        elif event == 'Назад':
            window.close()
            break
        elif event == 'Далее':
            if not values['summ']:
                Gui.popup('Вы не ввели обязательное поле:\nСумма по заявлению', title='Пустое поле')
            else:
                try:
                    summ = float(values['summ'].replace(',', '.'))
                except ValueError:
                    Gui.popup('Вы ввели не числовое значение:\nСумма по заявлению', title='Ошибка')
                else:
                    data['summ'] = summ
                if values['yandex']:
                    try:
                        yandex_summ = sum(float(ya.replace(',', '.')) for ya in values['yandex'].split('\n'))
                    except ValueError:
                        Gui.popup('Вы ввели не числовое значение:\nЯндекс еда', title='Ошибка')
                    else:
                        data['yandex'] = yandex_summ
                else:
                    data['yandex'] = 0.0
                if values['delivery']:
                    try:
                        delivery_summ = sum(float(ya.replace(',', '.')) for ya in values['delivery'].split('\n'))
                    except ValueError:
                        Gui.popup('Вы ввели не числовое значение:\nЯндекс еда', title='Ошибка')
                    else:
                        data['delivery'] = delivery_summ
                else:
                    data['delivery'] = 0.0
                window.hide()
                res = eda_5(data)
                if res == 'back':
                    return 'back'
                window.un_hide()


def run(data):
    try:
        return main(data)
    except Exception as e:
        Gui.PopupAnimated(None)
        tb = traceback.format_exc()
        Gui.popup_error(f'An error happened. Here is the info:', e, tb)
