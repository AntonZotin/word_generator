import PySimpleGUI as Gui

from src.utils.strings import EDA_4_WINDOW, SUCCESS

yandex_index = 1
delivery_index = 1


def get_eda_4_window(data):
    global yandex_index, delivery_index
    yandex_index = 1
    delivery_index = 1
    yandex = [[Gui.Text('Яндекс еда'), Gui.Button('+', key='yandex_add')],
              [Gui.Frame('', [[Gui.InputText(size=(20, 1), key=f'yandex{yandex_index}')]], key='yandex', border_width=0)]]

    delivery = [[Gui.Text('Деливери'), Gui.Button('+', key='delivery_add')],
                [Gui.Frame('', [[Gui.InputText(size=(20, 1), key=f'delivery{delivery_index}')]], key='delivery', border_width=0)]]
    yandex_index += 1
    delivery_index += 1

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


def eda_4_event(window, event, values, data):
    global yandex_index, delivery_index
    if event == 'yandex_add':
        window.extend_layout(window['yandex'], [[Gui.InputText(size=(20, 1), key=f'yandex{yandex_index}')]])
        yandex_index += 1
    elif event == 'delivery_add':
        window.extend_layout(window['delivery'], [[Gui.InputText(size=(20, 1), key=f'delivery{delivery_index}')]])
        delivery_index += 1
    elif event == 'Далее':
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

            data['yandex'] = 0.0
            for y in range(yandex_index):
                if values.get(f'yandex{y}'):
                    try:
                        data['yandex'] += float(values.get(f'yandex{y}'))
                    except ValueError:
                        error = True
                        Gui.popup('Вы ввели не числовое значение:\nЯндекс еда', title='Ошибка')

            data['delivery'] = 0.0
            for y in range(delivery_index):
                if values.get(f'delivery{y}'):
                    try:
                        data['delivery'] += float(values.get(f'delivery{y}'))
                    except ValueError:
                        error = True
                        Gui.popup('Вы ввели не числовое значение:\nДеливери', title='Ошибка')

            if not error:
                return SUCCESS, data
