import PySimpleGUI as Gui

from src.utils.strings import EDA_4_WINDOW, SUCCESS


def get_eda_4_window():
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
        [Gui.Submit(button_text='Далее'), Gui.Submit(button_text='Назад'), Gui.Submit(button_text='Сбросить все')]
    ]
    return Gui.Window(EDA_4_WINDOW, layout, grab_anywhere=False,
                      element_justification='c').Finalize()


def eda_4_event(window, event, values):
    if event == 'Далее':
        if not values['summ']:
            Gui.popup('Вы не ввели обязательное поле:\nСумма по заявлению', title='Пустое поле')
        else:
            data = {}
            error = False
            try:
                summ = float(values['summ'].replace(',', '.'))
            except ValueError:
                error = True
                Gui.popup('Вы ввели не числовое значение:\nСумма по заявлению', title='Ошибка')
            else:
                data['summ'] = summ
            if values.get('yandex'):
                try:
                    yandex_summ = sum(float(ya.replace(',', '.')) for ya in values['yandex'].split('\n'))
                except ValueError:
                    error = True
                    Gui.popup('Вы ввели не числовое значение:\nЯндекс еда', title='Ошибка')
                else:
                    data['yandex'] = yandex_summ
            else:
                data['yandex'] = 0.0
            if values.get('delivery'):
                try:
                    delivery_summ = sum(float(ya.replace(',', '.')) for ya in values['delivery'].split('\n'))
                except ValueError:
                    error = True
                    Gui.popup('Вы ввели не числовое значение:\nЯндекс еда', title='Ошибка')
                else:
                    data['delivery'] = delivery_summ
            else:
                data['delivery'] = 0.0

            if not error:
                return SUCCESS, data
