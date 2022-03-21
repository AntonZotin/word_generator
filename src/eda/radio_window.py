import PySimpleGUI as Gui
import pyperclip

from src.utils.checklist_strings import header_max_symbols, text_max_symbols
from src.utils.strings import SUCCESS
from src.utils.utils import extract_radio_values, onKeyRelease


def get_radio_eda(data, radio_dict, title):
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
    window.TKroot.bind_all("<Key>", onKeyRelease, "+")
    return window


def radio_eda(window, event, values, radios, radios_mapping, key):
    if 'RADIO' in str(event):
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
    elif event == 'Далее':
        return SUCCESS, {key: extract_radio_values(values, radios, radios_mapping)}
