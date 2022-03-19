import re

import PySimpleGUI as Gui

from src.utils.strings import TEMPLATE_WINDOW, MODAL_CLOSE

parent_window = None
parent_values = None
static_comments_array = []


def wrap_text(text):
    if len(text) < 30:
        return text
    else:
        return '\n'.join(re.findall('.{1,30}', text))


def get_template_window(comments_array, event, p_window, p_values):
    global parent_window, parent_values, static_comments_array
    parent_window = p_window
    parent_values = p_values
    static_comments_array = comments_array
    index = event.replace('TEMPLATE', '')
    template_layout = [
        [Gui.Text('Поиск'), Gui.Input(size=(80, 1), enable_events=True, key='search', pad=(10, 10))],
        [Gui.Listbox([ca for ca in comments_array], size=(100, 30), enable_events=True, key='comments',
                     horizontal_scroll=True)],
        [Gui.Submit(button_text='Выбрать', key=f'Select{index}'),
         Gui.Submit(button_text='Закрыть', key='Confirm')]]
    return Gui.Window(TEMPLATE_WINDOW, template_layout, modal=True,
                      element_justification='c').Finalize()


def template_event(window, event, values, data):
    global parent_window
    if event == 'search':
        search = values['search']
        new_values = [sca for sca in static_comments_array if search in sca]
        window['comments'].update(new_values)
    elif event.startswith('Select'):
        try:
            index = event.replace('Select', '')
            res_comment = parent_values.get(f'TEXT{index}', '')
            if res_comment and not res_comment.endswith('\n'):
                res_comment += '\n'
            res_comment += values['comments'][0] + '\n'
            parent_window[f'TEXT{index}'].update(res_comment)
            window.close()
            return MODAL_CLOSE
        except IndexError:
            Gui.popup('Вы не выбрали шаблон', title='')
