import re
import traceback

import PySimpleGUI as Gui
import pyperclip

from src.checklist_strings import eda_crits
from src.generate_doc import main_generate_word
from src.generate_excel import main_insert_and_sort_xlsx
from src.strings import COMMENTS_FILE, END_OF_COMMENT

header_max_symbols = 50
text_max_symbols = 80


def filter_key(name):
    matched = re.match('RADIO(\d+)-(\w+)', name).groups()
    return matched[0] if matched[1] == 'no' else None


def separate_comment(comment):
    return [re.sub('^\d+[.)\s+]+', '', c) for c in comment.strip().split('\n')]


def main(data):
    init_text = ""
    for d in data['error_docs']:
        init_text += f"{d}\n"
    for c in data['error_crits']:
        init_text += f"{c}\n"
    with open(COMMENTS_FILE, 'r+') as t:
        comments_file = t.read().strip()
        comments_array = set(e.strip() for e in
                             filter(lambda el: el, comments_file.split(END_OF_COMMENT))) if comments_file else set()
    right = ["right_menu", ["Копировать", "Вставить"]]
    layout = [
        [Gui.Text('Комментарий', size=(10, 1)), Gui.Multiline(size=(80, 30), key='comment', disabled=False, right_click_menu=right, default_text=init_text)],
        [Gui.Text('Шаблон комментария', size=(16, 1)), Gui.Button('Выбрать', size=(10, 1), key='template')],
        [Gui.Submit(button_text='Сгенерировать'), Gui.Submit(button_text='Назад')]
    ]
    window = Gui.Window('Предварительный просмотр замечаний', layout, grab_anywhere=False, element_justification='c').Finalize()

    templates_active = False
    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit', 'Cancel', 'Закрыть'):
            return 0
        elif event == 'Назад':
            window.close()
            break
        elif event == "Копировать":
            pyperclip.copy(window['comment'].Widget.selection_get())
        elif event == "Вставить":
            window['comment'].update(values['comment'] + pyperclip.paste())
        elif templates_active:
            template_event, template_values = template_window.Read(timeout=100)
            if template_event in (None, 'Exit', 'Cancel'):
                templates_active = False
                template_window.close()
            elif template_event == 'Select template':
                try:
                    tv = list(filter(lambda k: template_values[k], template_values.keys()))
                    res_comment = values['comment']
                    if not res_comment.endswith('\n'):
                        res_comment += '\n'
                    res_comment += tv[0] + '\n'
                    window['comment'].update(res_comment)
                    templates_active = False
                    template_window.close()
                except IndexError:
                    Gui.popup('Вы не выбрали шаблон', title='')
        elif not templates_active and event == 'template':
            templates_active = True
            template_layout = [
                [Gui.Col([[Gui.Radio(ca, default=False, group_id='2', key=ca,
                                     text_color='black', background_color='white')] for ca in comments_array],
                         background_color='white', size=(660, 500), scrollable=True)],
                [Gui.Text('', size=(30, 1)), Gui.Submit(button_text='Выбрать', key='Select template'),
                 Gui.Submit(button_text='Закрыть', key='Cancel')]]
            template_window = Gui.Window('Выбор шаблона', template_layout)
        elif event == 'Сгенерировать':
            comment = values['comment']
            if comment:
                for c in separate_comment(comment):
                    if c not in comments_array:
                        with open(COMMENTS_FILE, 'a+') as f:
                            f.write('%s%s\n' % (c, END_OF_COMMENT))
                        comments_array.add(c)
                data['comment'] = comment
            main_generate_word(data)
            # main_insert_and_sort_xlsx(data)


def run(data):
    try:
        main(data)
    except Exception as e:
        Gui.PopupAnimated(None)
        tb = traceback.format_exc()
        Gui.popup_error(f'An error happened. Here is the info:', e, tb)
