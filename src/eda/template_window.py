import PySimpleGUI as Gui

from src.utils.strings import TEMPLATE_WINDOW, MODAL_CLOSE

parent_window = None
parent_values = None


def get_template_window(comments_array, event, p_window, p_values):
    global parent_window, parent_values
    parent_window = p_window
    parent_values = p_values
    index = event.replace('TEMPLATE', '')
    template_layout = [
        [Gui.Col([[Gui.Radio(ca, default=False, group_id='2', key=ca,
                             text_color='black', background_color='white')] for ca in comments_array],
                 background_color='white', size=(950, 780), scrollable=True)],
        [Gui.Submit(button_text='Выбрать', key=f'Select{index}'),
         Gui.Submit(button_text='Закрыть', key='Confirm')]]
    return Gui.Window(TEMPLATE_WINDOW, template_layout, modal=True,
                      element_justification='c').Finalize()


def template_event(window, event, values, data):
    global parent_window
    if event.startswith('Select'):
        try:
            index = event.replace('Select', '')
            tv = list(filter(lambda k: values[k], values.keys()))
            res_comment = parent_values.get(f'TEXT{index}', '')
            if res_comment and not res_comment.endswith('\n'):
                res_comment += '\n'
            res_comment += tv[0] + '\n'
            parent_window[f'TEXT{index}'].update(res_comment)
            window.close()
            return MODAL_CLOSE
        except IndexError:
            Gui.popup('Вы не выбрали шаблон', title='')
