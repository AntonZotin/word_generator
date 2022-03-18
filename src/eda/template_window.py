
import PySimpleGUI as Gui

from src.utils.strings import SUCCESS, TEMPLATE_WINDOW


def get_template_window(comments_array, event):
    index = event.replace('TEMPLATE', '')
    template_layout = [
        [Gui.Col([[Gui.Radio(ca, default=False, group_id='2', key=ca,
                             text_color='black', background_color='white')] for ca in comments_array],
                 background_color='white', size=(660, 500), scrollable=True)],
        [Gui.Text('', size=(30, 1)), Gui.Submit(button_text='Выбрать', key=f'Select{index}'),
         Gui.Submit(button_text='Закрыть', key='Confirm')]]
    return Gui.Window(TEMPLATE_WINDOW, template_layout, modal=True)


def template_event(parent_window, event, values):
    if event.startswith('Select'):
        try:
            index = event.replace('Select', '')
            tv = list(filter(lambda k: values[k], values.keys()))
            res_comment = values.get(f'TEXT{index}', '')
            if res_comment and not res_comment.endswith('\n'):
                res_comment += '\n'
            res_comment += tv[0] + '\n'
            parent_window[f'TEXT{index}'].update(res_comment)
            return SUCCESS, None
        except IndexError:
            Gui.popup('Вы не выбрали шаблон', title='')
