import PySimpleGUI as Gui
import pyperclip

from src.utils.checklist_strings import eda_crits, eda_docs
from src.utils.generate_doc import main_generate_word
from src.utils.generate_excel import main_insert_and_sort_xlsx
from src.utils.strings import COMMENTS_FILE, END_OF_COMMENT, XLSX_FILE_EDA, EDA_5_WINDOW, CLEAR
from src.utils.utils import separate_comment


def get_eda_5_window(error_docs, error_crits):
    init_text = ""
    count = 1
    for d in error_docs:
        init_text += f"{count}. {d}\n"
        count += 1
    for c in error_crits:
        init_text += f"{count}. {c}\n"
        count += 1
    right = ["right_menu", ["Копировать", "Вставить"]]
    layout = [
        [Gui.Text('Комментарий', size=(10, 1)),
         Gui.Multiline(size=(80, 30), key='comment', disabled=False, right_click_menu=right, default_text=init_text)],
        [Gui.Text('Шаблон комментария', size=(16, 1)), Gui.Button('Выбрать', size=(10, 1), key='TEMPLATE0')],
        [Gui.Submit(button_text='Сгенерировать'), Gui.Submit(button_text='Назад'),
         Gui.Submit(button_text='Сбросить все')]
    ]
    return Gui.Window(EDA_5_WINDOW, layout, grab_anywhere=False, element_justification='c').Finalize()


def eda_5_event(window, event, values, comments_array):
    if event == "Копировать":
        pyperclip.copy(window['comment'].Widget.selection_get())
    elif event == "Вставить":
        window['comment'].update(values['comment'] + pyperclip.paste())
    elif event == 'Сгенерировать':
        data = {}
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
            Gui.popup(f'Не найден реестр. Рядом с папкой программы должен лежать файл {XLSX_FILE_EDA}.xlsx.',
                      title='Нет прав')

        if success:
            Gui.popup('Заключение успешно сгенерировано.', title='Успешно')
            return CLEAR, None
