import PySimpleGUI as Gui
import pyperclip

from src.utils.checklist_strings import eda_crits, eda_docs
from src.utils.decorators import exception_handler
from src.utils.generate_doc import main_generate_word
from src.utils.generate_excel import main_insert_and_sort_xlsx
from src.utils.strings import COMMENTS_FILE, END_OF_COMMENT, XLSX_FILE_EDA, EDA_5_WINDOW
from src.utils.utils import separate_comment


@exception_handler
def eda_5(data):
    init_text = ""
    count = 1
    for d in data['error_docs']:
        init_text += f"{count}. {d}\n"
        count += 1
    for c in data['error_crits']:
        init_text += f"{count}. {c}\n"
        count += 1
    with open(COMMENTS_FILE, 'r+') as t:
        comments_file = t.read().strip()
        comments_array = set(e.strip() for e in
                             filter(lambda el: el, comments_file.split(END_OF_COMMENT))) if comments_file else set()
    right = ["right_menu", ["Копировать", "Вставить"]]
    layout = [
        [Gui.Text('Комментарий', size=(10, 1)), Gui.Multiline(size=(80, 30), key='comment', disabled=False, right_click_menu=right, default_text=init_text)],
        [Gui.Text('Шаблон комментария', size=(16, 1)), Gui.Button('Выбрать', size=(10, 1), key='template')],
        [Gui.Submit(button_text='Сгенерировать'), Gui.Submit(button_text='Назад'), Gui.Submit(button_text='Сбросить все')]
    ]
    window = Gui.Window(EDA_5_WINDOW, layout, grab_anywhere=False, element_justification='c').Finalize()

    templates_active = False
    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit', 'Cancel', 'Закрыть'):
            return 0
        elif event == 'Назад':
            window.close()
            break
        elif event == 'Сбросить все':
            window.close()
            return 'back'
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
            template_window = Gui.Window('Выбор шаблона', template_layout, modal=True)
        elif event == 'Сгенерировать':
            comment = values['comment']
            if comment:
                docs = [d for d, _, _ in eda_docs]
                crits = [c for c, _, _ in eda_crits]
                for c in separate_comment(comment):
                    if c not in comments_array and c not in docs and c not in crits:
                        with open(COMMENTS_FILE, 'a+') as f:
                            f.write('%s%s\n' % (c, END_OF_COMMENT))
                        comments_array.add(c)
                data['comment'] = comment
            data['postanovlenie'] = 'Д'
            success = False
            try:
                main_generate_word(data)
                success = True
            except PermissionError:
                Gui.popup('Заключение сейчас открыто в Microsoft Word, перезапись невозможна.', title='Нет прав')

            try:
                main_insert_and_sort_xlsx(data)
            except PermissionError:
                Gui.popup('Реестр сейчас открыт в другой программе, запись в него невозможна.', title='Нет прав')
            except FileNotFoundError:
                Gui.popup(f'Не найден реестр. Рядом с папкой программы должен лежать файл {XLSX_FILE_EDA}.xlsx.', title='Нет прав')

            if success:
                Gui.popup('Заключение успешно сгенерировано.', title='Успешно')
                window.close()
                return 'back'
