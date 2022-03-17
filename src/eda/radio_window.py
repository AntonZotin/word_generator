from src.checklist_strings import header_max_symbols, text_max_symbols
from src.strings import COMMENTS_FILE, END_OF_COMMENT
import PySimpleGUI as Gui
import pyperclip

from src.utils import extract_radio_values


def radio_eda(data, radio_dict, title, data_key, next_window):
    with open(COMMENTS_FILE, 'r+') as t:
        comments_file = t.read().strip()
        comments_array = set(e.strip() for e in
                             filter(lambda el: el, comments_file.split(END_OF_COMMENT))) if comments_file else set()
    arr = []
    radios = {}
    index = 1
    for c, perm, maybe in radio_dict:
        if c.startswith('HEADER '):
            c = c.replace('HEADER ', '')
            arr += [
                [Gui.Text(c, size=(66, int(len(c) / header_max_symbols)), justification='center',
                          font=("Helvetica", 18), relief=Gui.RELIEF_RIDGE)],
                [Gui.Text('-' * 230)]
            ]
        elif data['type'] in perm:
            c = c.replace('\\n', '\n')
            height = int(len(c) / text_max_symbols)
            height += int(c.count('\n') / 5)
            predstav = 'для представителя' in c
            width = 69 if predstav else 85
            prefix_arr = [Gui.Text(c, size=(width, height), key=f"RADIO{index}-text"), ]
            if predstav:
                prefix_arr.append(Gui.Radio('Сам заявитель', f"RADIO{index}", key=f"RADIO{index}-yeah",
                                            enable_events=True))
            comment_frame = [
                [Gui.Multiline(size=(110, 3), key=f'TEXT{index}', disabled=False,
                               right_click_menu=["right_menu", [f"Копировать из {index}", f"Вставить в {index}"]]),
                 Gui.Button('Выбрать шаблон', size=(15, 1), key=f'TEMPLATE{index}')],
                [Gui.Text('-' * 230)],
            ]
            arr += [[
                Gui.Col([
                    [*prefix_arr, Gui.VerticalSeparator(),
                     Gui.Radio('да', f"RADIO{index}", key=f"RADIO{index}-yes", enable_events=True),
                     Gui.Radio('нет', f"RADIO{index}", key=f"RADIO{index}-{'maybe' if maybe else 'no'}",
                               enable_events=True),
                     Gui.Submit(button_text='Комментарий', key=f"BUTTON-O-{index}", visible=True, size=(12, 1)),
                     Gui.Submit(button_text='Закрыть', key=f"BUTTON-C-{index}", visible=False, size=(12, 1),
                                button_color='#d0d0d0')],
                    [Gui.Text('-' * 230)],
                    [Gui.Frame('Комментарий', comment_frame, key=f'COMMENT{index}', size=(926, 97), border_width=0)],
                ], key=f'COL{index}')
            ]]
            radios[str(index)] = c
            index += 1

    layout = [
        [Gui.Col(arr, size=(950, 780), scrollable=True, vertical_scroll_only=True)],
        [Gui.Submit(button_text='Далее'), Gui.Submit(button_text='Назад'), Gui.Submit(button_text='Сбросить все')]
    ]
    window = Gui.Window(title, layout, grab_anywhere=False,
                        element_justification='c').Finalize()
    for i in range(1, index):
        window[f'COMMENT{i}'].hide_row()

    templates_active = False
    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit', 'Cancel', 'Закрыть'):
            return 0
        elif event == 'Сбросить все':
            window.close()
            return 'back'
        elif 'RADIO' in str(event):
            res = event.replace('RADIO', '').split('-')
            if res[1] == 'yes' or res[1] == 'yeah':
                window[f"RADIO{res[0]}-text"].update(text_color='#37ff5a')
            elif res[1] == 'maybe':
                window[f"RADIO{res[0]}-text"].update(text_color='#ffa500')
            else:
                window[f"RADIO{res[0]}-text"].update(text_color='#ff4f4f')
        elif str(event).startswith('BUTTON'):
            _, status, index = event.split('-')
            if status == 'O':
                window[f"BUTTON-O-{index}"].update(visible=False)
                window[f"BUTTON-C-{index}"].update(visible=True)
                window[f'COMMENT{index}'].unhide_row()
                window.refresh()
            else:
                window[f"BUTTON-C-{index}"].update(visible=False)
                window[f"BUTTON-O-{index}"].update(visible=True)
                window[f'COMMENT{index}'].hide_row()
                window.refresh()
        elif event.startswith("Копировать"):
            index = event.replace('Копировать из ', '')
            pyperclip.copy(window[f'TEXT{index}'].Widget.selection_get())
        elif event.startswith("Вставить"):
            index = event.replace('Вставить в ', '')
            window[f'TEXT{index}'].update(values[f'TEXT{index}'] + pyperclip.paste())
        elif templates_active:
            template_event, template_values = template_window.Read(timeout=100)
            if template_event in (None, 'Exit', 'Cancel'):
                templates_active = False
                template_window.close()
            elif template_event.startswith('Select'):
                try:
                    index = template_event.replace('Select', '')
                    tv = list(filter(lambda k: template_values[k], template_values.keys()))
                    res_comment = values.get(f'TEXT{index}', '')
                    if res_comment and not res_comment.endswith('\n'):
                        res_comment += '\n'
                    res_comment += tv[0] + '\n'
                    window[f'TEXT{index}'].update(res_comment)
                    templates_active = False
                    template_window.close()
                except IndexError:
                    Gui.popup('Вы не выбрали шаблон', title='')
        elif not templates_active and event.startswith('TEMPLATE'):
            index = event.replace('TEMPLATE', '')
            templates_active = True
            template_layout = [
                [Gui.Col([[Gui.Radio(ca, default=False, group_id='2', key=ca,
                                     text_color='black', background_color='white')] for ca in comments_array],
                         background_color='white', size=(660, 500), scrollable=True)],
                [Gui.Text('', size=(30, 1)), Gui.Submit(button_text='Выбрать', key=f'Select{index}'),
                 Gui.Submit(button_text='Закрыть', key='Cancel')]]
            template_window = Gui.Window('Выбор шаблона', template_layout)
        elif event == 'Назад':
            window.close()
            break
        elif event == 'Далее':
            data[data_key] = extract_radio_values(values, radios)
            window.hide()
            res = next_window(data)
            if res == 'back':
                return 'back'
            elif res == 0:
                return 0
            window.un_hide()
