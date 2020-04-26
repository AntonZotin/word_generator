import sys

import PySimpleGUI as Gui
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt
from datetime import datetime

required_fields = {
    'name': 'Наименование компании',
    'inn': 'ИНН',
    'number': 'Номер заявки',
    'date': 'Дата заявки',
    'has_comment': 'Соответствие заявки',
    'comment': 'Комментарий',
}

numeric_fields = ['inn', 'number']

tab = '            '
text1 = 'Юридическим отделом государственного казенного учреждения «Центр реализации программ поддержки и ' \
        'развития малого и среднего предпринимательства Республики Татарстан» (далее – Учреждение) проверена заявка '
text2 = ' (ИНН '
text3 = ') № '
text4 = ' от '
text5 = ' на предмет соответствия требованиям Порядка предоставления субсидий на возмещение ' \
       'затрат, связанных с уплатой процентов по кредитам, привлеченным в российских кредитных организациях, ' \
       'утвержденного постановлением Кабинета Министров Республики Татарстан от 24.09.2019 № 873 «Об утверждении ' \
       'Порядка предоставления субсидий на возмещение затрат, связанных с уплатой процентов по кредитам, привлеченным ' \
       'в российских кредитных организациях» (далее – Порядок).'
success = 'По итогам проверки замечания не выявлены.'
fail = 'По итогам проверки выявлены следующие замечания:'
specialist = 'Главный специалист						              Е.Р. Зотина'
footer = 'Дата: '

HAS_NO_COMMENT = 'Соответствует'
HAS_COMMENT = 'Не соответствует'
END_OF_COMMENT = '<END_OF_COMMENT>'
COMMENTS_FILE = 'templates.txt'


def main_generate_word(name, inn, number, date, has_comment, comment):
    if has_comment == HAS_COMMENT:
        comment = comment.replace("\n", "\t\n" + tab)
    paragraph1 = f'{tab}{text1}{name}{text2}{inn}{text3}{number}{text4}{date}{text5}\t\n' \
        f'{tab}{fail if has_comment == HAS_COMMENT else success}\t\n' \
        f'{tab}{comment if has_comment == HAS_COMMENT else ""}\t\n'
    paragraph2 = f'{specialist}\n\n\n'
    paragraph3 = f'{footer}{datetime.today().strftime("%d.%m.%Y")}'

    document = Document()

    obj_styles = document.styles
    obj_charstyle = obj_styles.add_style('Main title', WD_STYLE_TYPE.CHARACTER)
    obj_font = obj_charstyle.font
    obj_font.size = Pt(14)
    obj_font.name = 'Times New Roman'
    obj_charstyle = obj_styles.add_style('Middle paragraph', WD_STYLE_TYPE.CHARACTER)
    obj_font = obj_charstyle.font
    obj_font.size = Pt(12)
    obj_font.name = 'Times New Roman'
    obj_charstyle = obj_styles.add_style('Last paragraph', WD_STYLE_TYPE.CHARACTER)
    obj_font = obj_charstyle.font
    obj_font.size = Pt(8)
    obj_font.name = 'Times New Roman'

    t = document.add_paragraph('')
    t.add_run('ЗАКЛЮЧЕНИИЕ ЮРИДИЧЕСКОГО ОТДЕЛА', style='Main title').bold = True
    t.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    p1 = document.add_paragraph('')
    p1.add_run(paragraph1, style='Middle paragraph')
    p1.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY

    p2 = document.add_paragraph('')
    p2.add_run(paragraph2, style='Middle paragraph').bold = True
    p2.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT

    p3 = document.add_paragraph('')
    p3.add_run(paragraph3, style='Last paragraph')
    p3.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT

    document.save("%s %s.docx" % (name.replace('\"', '\''), number[-4:]))


def main():
    with open(COMMENTS_FILE, 'r') as t:
        comments_file = t.read().strip()
        comments_array = [e.strip() for e in filter(lambda el: el, comments_file.split(END_OF_COMMENT))] if comments_file else []
    layout = [
        [Gui.Text('Наименование компании', size=(20, 1)), Gui.InputText(size=(42, 1), key='name')],
        [Gui.Text('ИНН', size=(20, 1)), Gui.Input(size=(42, 1), key='inn', enable_events=True)],
        [Gui.Text('Номер заявки', size=(20, 1)), Gui.Input(size=(42, 1), key='number', enable_events=True)],
        [Gui.Text('Дата заявки', size=(20, 1)), Gui.Input(size=(42, 1), key='date', enable_events=True)],
        [Gui.Text('_' * 68)],
        [Gui.Text('Соответствие заявки', size=(20, 1)), Gui.Combo([HAS_NO_COMMENT, HAS_COMMENT], size=(40, 1),
                                                                  readonly=True, key='has_comment')],
        [Gui.Text('Комментарий', size=(20, 1)), Gui.Multiline(size=(40, 10), key='comment')],
        [Gui.Text('Шаблон комментария', size=(20, 1)), Gui.Button('Выбрать', size=(10, 1), key='template')],
        [Gui.Text('', size=(25, 1)), Gui.Submit(button_text='Сгенерировать')]
    ]

    window = Gui.Window('Word generator', layout)

    templates_active = False
    while True:
        event, values = window.read(timeout=100)
        print(event, values)
        if event in (None, 'Exit', 'Cancel', 'Закрыть'):
            return 0
        elif templates_active:
            template_event, template_values = template_window.Read(timeout=100)
            if template_event in (None, 'Exit', 'Cancel'):
                templates_active = False
                template_window.close()
            elif template_event == 'Select template':
                try:
                    window['comment'].update(template_values['template'][0])
                    templates_active = False
                    template_window.close()
                except IndexError:
                    Gui.popup('Вы не выбрали шаблон', title='')
        elif not templates_active and event == 'template':
            if values['has_comment'] == HAS_COMMENT:
                templates_active = True
                template_layout = [
                    [Gui.Listbox([*comments_array], size=(100, 30), key='template')],
                    [Gui.Text('', size=(36, 1)), Gui.Submit(button_text='Выбрать', key='Select template'),
                     Gui.Submit(button_text='Закрыть', key='Cancel')]]
                template_window = Gui.Window('Выбор шаблона', template_layout)
            else:
                Gui.popup('Выбери соответствие заявки: Не соответствует', title='Статус заявки')
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
            if not name: required_errors.append(required_fields['name'])
            inn = values['inn']
            if not inn: required_errors.append(required_fields['inn'])
            number = values['number']
            if not number: required_errors.append(required_fields['number'])
            date = values['date']
            if not date: required_errors.append(required_fields['date'])
            has_comment = values['has_comment']
            if not has_comment: required_errors.append(required_fields['has_comment'])
            comment = values['comment'].strip()
            if not comment and has_comment: required_errors.append(required_fields['comment'])

            if not required_errors:
                if comment not in comments_array:
                    with open(COMMENTS_FILE, 'a') as f:
                        f.write('%s%s\n' % (comment, END_OF_COMMENT))
                    comments_array.append(comment)
                main_generate_word(name, inn, number, date, has_comment, comment)
            else:
                Gui.popup('Вы не ввели обязательные поля:\n%s' % ', '.join(required_errors), title='Пустые поля')


if __name__ == '__main__':
    sys.exit(main())
