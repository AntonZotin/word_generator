import re
import sys
import traceback

import pyperclip
import PySimpleGUI as Gui

from src.images import splash
from src.generate_doc import main_generate_word
from src.generate_excel import main_insert_and_sort_xlsx
from src.strings import specialists, postanovleniya, COMMENTS_FILE, END_OF_COMMENT, HAS_NO_COMMENT, HAS_COMMENT

required_fields = {
    'name': 'Наименование компании',
    'inn': 'ИНН',
    'number': 'Номер заявки',
    'date': 'Дата заявки',
    'ispolnitel': 'Исполнитель',
    'postanovlenie': 'Постановление',
    'has_comment': 'Соответствие заявки',
    'comment': 'Комментарий',
}

numeric_fields = ['inn', 'number']


def separate_comment(comment):
    return [re.sub('^\d+[.)\s+]+', '', c) for c in comment.strip().split('\n')]


def main():
    multiline_disabled = True
    Gui.PopupAnimated(splash)
    with open(COMMENTS_FILE, 'r+') as t:
        comments_file = t.read().strip()
        comments_array = set(e.strip() for e in
                             filter(lambda el: el, comments_file.split(END_OF_COMMENT))) if comments_file else set()
    right = ["right_menu", ["Копировать", "Вставить"]]
    layout = [
        [Gui.Text('Наименование компании', size=(20, 1)), Gui.InputText(size=(42, 1), key='name')],
        [Gui.Text('ИНН', size=(20, 1)), Gui.Input(size=(42, 1), key='inn', enable_events=True)],
        [Gui.Text('Номер заявки', size=(20, 1)), Gui.Input(size=(42, 1), key='number', enable_events=True)],
        [Gui.Text('Дата заявки', size=(20, 1)), Gui.Input(size=(42, 1), key='date', enable_events=True)],
        [Gui.Text('Исполнитель', size=(20, 1)), Gui.Combo([*specialists.keys()], size=(40, 1),
                                                          readonly=True, key='ispolnitel')],
        [Gui.Text('Постановление', size=(20, 1)), Gui.Combo([*postanovleniya.keys()], size=(40, 1),
                                                            readonly=True, key='postanovlenie')],
        [Gui.Text('_' * 68)],
        [Gui.Text('Соответствие заявки', size=(20, 1)),
         Gui.Radio(HAS_NO_COMMENT, default=True, group_id='1', key=HAS_NO_COMMENT),
         Gui.Radio(HAS_COMMENT, default=False, group_id='1', key=HAS_COMMENT)],
        [Gui.Text('Комментарий', size=(20, 1)), Gui.Multiline(size=(40, 10), key='comment', disabled=multiline_disabled, right_click_menu=right)],
        [Gui.Text('Шаблон комментария', size=(20, 1)), Gui.Button('Выбрать', size=(10, 1), key='template')],
        [Gui.Text('', size=(25, 1)), Gui.Submit(button_text='Сгенерировать'), Gui.Submit(button_text='Назад')]
    ]

    Gui.PopupAnimated(None)
    window = Gui.Window('Word generator', layout, grab_anywhere=False).Finalize()

    window[HAS_NO_COMMENT].bind('<Button-1>', '')
    window[HAS_COMMENT].bind('<Button-1>', '')

    templates_active = False
    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit', 'Cancel', 'Закрыть'):
            return 0
        elif event == "Копировать":
            if multiline_disabled:
                Gui.popup('Выбери соответствие заявки: Не соответствует', title='Статус заявки')
            else:
                pyperclip.copy(window['comment'].Widget.selection_get())
        elif event == "Вставить":
            if multiline_disabled:
                Gui.popup('Выбери соответствие заявки: Не соответствует', title='Статус заявки')
            else:
                window['comment'].update(values['comment'] + pyperclip.paste())
                window['comment'].update(disabled=False)
        elif templates_active:
            template_event, template_values = template_window.Read(timeout=100)
            if template_event in (None, 'Exit', 'Cancel'):
                templates_active = False
                template_window.close()
            elif template_event == 'Select template':
                try:
                    tv = list(filter(lambda k: template_values[k], template_values.keys()))
                    window['comment'].update(re.sub('\n$', '', values['comment'], 1) + tv[0] + '\n')
                    templates_active = False
                    template_window.close()
                    window['comment'].update(disabled=False)
                except IndexError:
                    Gui.popup('Вы не выбрали шаблон', title='')
        elif not templates_active and event == 'template':
            if values[HAS_COMMENT]:
                templates_active = True
                template_layout = [
                    [Gui.Col([[Gui.Radio(ca, default=False, group_id='2', key=ca,
                                         text_color='black', background_color='white')] for ca in comments_array],
                             background_color='white', size=(600, 500), scrollable=True)],
                    [Gui.Text('', size=(30, 1)), Gui.Submit(button_text='Выбрать', key='Select template'),
                     Gui.Submit(button_text='Закрыть', key='Cancel')]]
                template_window = Gui.Window('Выбор шаблона', template_layout)
            else:
                Gui.popup('Выбери соответствие заявки: Не соответствует', title='Статус заявки')
        elif event == HAS_NO_COMMENT:
            multiline_disabled = True
            window['comment'].update('', disabled=multiline_disabled)
        elif event == HAS_COMMENT:
            multiline_disabled = False
            window['comment'].update(disabled=multiline_disabled)
        elif event in numeric_fields and values[event] and values[event][-1] not in '0123456789':
            window[event].update(values[event][:-1])
        elif event == 'date' and values[event]:
            if len(values[event]) == 2 or len(values[event]) == 5:
                window[event].update(values[event] + '.')
            elif len(values[event]) == 11:
                window[event].update(values[event][:-1])
        elif event == 'Сгенерировать':
            required_errors = []
            name = values['name']
            window['name'].update('')
            if not name: required_errors.append(required_fields['name'])
            inn = values['inn']
            window['inn'].update('')
            if not inn: required_errors.append(required_fields['inn'])
            number = values['number']
            window['number'].update('')
            if not number: required_errors.append(required_fields['number'])
            date = values['date']
            window['date'].update('')
            if not date: required_errors.append(required_fields['date'])
            ispolnitel = values['ispolnitel']
            window['ispolnitel'].update('')
            if not ispolnitel: required_errors.append(required_fields['ispolnitel'])
            postanovlenie = values['postanovlenie']
            window['postanovlenie'].update('')
            if not postanovlenie: required_errors.append(required_fields['postanovlenie'])
            comment = values['comment'].strip()
            window['comment'].update('')
            if not comment and values[HAS_COMMENT]: required_errors.append(required_fields['comment'])
            window[HAS_COMMENT].update(False)
            window[HAS_NO_COMMENT].update(True)

            if not required_errors:
                if comment:
                    for c in separate_comment(comment):
                        if c not in comments_array:
                            with open(COMMENTS_FILE, 'a+') as f:
                                f.write('%s%s\n' % (c, END_OF_COMMENT))
                            comments_array.add(c)
                main_generate_word(name, inn, number, date, ispolnitel, postanovlenie, values[HAS_COMMENT], comment)
                main_insert_and_sort_xlsx(name, inn, number, date, ispolnitel, postanovlenie)
            else:
                Gui.popup('Вы не ввели обязательные поля:\n%s' % ', '.join(required_errors), title='Пустые поля')
        elif event == 'Назад':
            window.close()
            break


def run():
    try:
        main()
    except Exception as e:
        Gui.PopupAnimated(None)
        tb = traceback.format_exc()
        Gui.popup_error(f'An error happened. Here is the info:', e, tb)


if __name__ == '__main__':
    sys.exit(run())