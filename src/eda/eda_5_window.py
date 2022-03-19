import PySimpleGUI as Gui
import pyperclip

from src.utils.checklist_strings import eda_docs_mapping, eda_crits_mapping, eda_docs, eda_crits
from src.utils.generate_doc import main_generate_word
from src.utils.generate_excel import main_insert_and_sort_xlsx
from src.utils.strings import COMMENTS_FILE, END_OF_COMMENT, XLSX_FILE_EDA, EDA_5_WINDOW, CLEAR
from src.utils.utils import separate_comment, find_in_comments


def get_eda_5_window(data):
    init_text = ""
    count = 1
    for d in data['error_docs']:
        init_text += f"{count}. {d}\n"
        count += 1
    for c in data['error_crits']:
        init_text += f"{count}. {c}\n"
        count += 1
    right = ["right_menu", ["Копировать", "Вставить"]]
    layout = [
        [Gui.Text('Комментарий', size=(10, 1)),
         Gui.Multiline(size=(80, 30), key='TEXT0', disabled=False, right_click_menu=right, default_text=init_text)],
        [Gui.Text('Шаблон комментария', size=(16, 1)), Gui.Button('Выбрать', size=(10, 1), key='TEMPLATE0')],
        [Gui.Submit(button_text='Сгенерировать'), Gui.Submit(button_text='Назад'),
         Gui.Submit(button_text='Сбросить все')]
    ]
    return Gui.Window(EDA_5_WINDOW, layout, grab_anywhere=False, element_justification='c').Finalize()


def eda_5_event(window, event, values, data):
    if event == "Копировать":
        pyperclip.copy(window['TEXT0'].Widget.selection_get())
    elif event == "Вставить":
        window['TEXT0'].update(values['TEXT0'] + pyperclip.paste())
    elif event == 'Сгенерировать':
        comment = values['TEXT0']
        if comment:
            with open(COMMENTS_FILE, 'r+', encoding='utf-8') as t:
                comments_file = t.read().strip()
                comments_array = set(e.strip() for e in filter(lambda el: el, comments_file.split(
                    END_OF_COMMENT))) if comments_file else set()
            docs = [d for d, _, _ in eda_docs]
            crits = [c for c, _, _ in eda_crits]
            docs_mapping = list(eda_docs_mapping.values())
            crits_mapping = list(eda_crits_mapping.values())
            for c in separate_comment(comment):
                if c not in comments_array and not find_in_comments(c, comments_array) and c not in docs \
                        and c not in crits and c not in docs_mapping and c not in crits_mapping:
                    with open(COMMENTS_FILE, 'a+', encoding='utf-8') as f:
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
            Gui.popup(f'Не найден реестр. Рядом с папкой программы должен лежать файл {XLSX_FILE_EDA}.xlsx.',
                      title='Нет прав')

        if success:
            Gui.popup('Заключение успешно сгенерировано.', title='Успешно')
            return CLEAR
