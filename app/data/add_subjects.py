# app/data/add_subjects.py

'''
Скрипт для добавления предметов в базу данных.

Этот скрипт добавляет предметы в таблицу 'subject', привязанные к соответствующим направлениям.
Предметы добавляются для направлений: Естественные науки, Общественные науки, Гуманитарные науки,
Технические науки, Спортивное направление и их подкатегории.

Перед выполнением убедитесь, что создано и настроено приложение Flask и база данных.

Чтобы выполнить скрипт, используйте команду:
    python app/data/add_subjects.py
'''

import sys
import os

# Устанавливаем путь до корня проекта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import create_app
from app.db import db
from app.db.models import Direction, Subject

# Функция для добавления предметов в базу данных
def add_subjects():
    # Список направлений и соответствующих предметов, их описания и демо-версии
    subjects_data = {
        'Естественные науки': [
            {'name': 'Математика', 'description': 'Изучение чисел, величин, структур и пространств.',
             'demo_version': 'https://example.com/demo/math'},
            {'name': 'Астрономия', 'description': 'Изучение космоса, звезд и планет.',
             'demo_version': 'https://example.com/demo/astronomy'},
            {'name': 'Биология', 'description': 'Наука о живых организмах и процессах жизни.',
             'demo_version': 'https://example.com/demo/biology'},
            {'name': 'География', 'description': 'Изучение Земли, её стран и природных явлений.',
             'demo_version': 'https://example.com/demo/geography'},
            {'name': 'Экология', 'description': 'Наука о взаимоотношениях живых существ и окружающей среды.',
             'demo_version': 'https://example.com/demo/ecology'},
            {'name': 'Физика', 'description': 'Изучение природы и законов, управляющих материальным миром.',
             'demo_version': 'https://example.com/demo/physics'},
            {'name': 'Химия', 'description': 'Наука о веществах и их превращениях.',
             'demo_version': 'https://example.com/demo/chemistry'}
        ],
        'Общественные науки': [
            {'name': 'Экономика', 'description': 'Наука об экономических процессах и их влиянии на общество.',
             'demo_version': 'https://example.com/demo/economics'},
            {'name': 'Обществознание', 'description': 'Изучение общества и его закономерностей.',
             'demo_version': 'https://example.com/demo/sociology'},
            {'name': 'Право', 'description': 'Наука о правовых нормах и их применении.',
             'demo_version': 'https://example.com/demo/law'},
            {'name': 'ОБЖ', 'description': 'Основы безопасности жизнедеятельности.',
             'demo_version': 'https://example.com/demo/obzh'}
        ],
        'Гуманитарные науки': [
            {'name': 'Русский язык', 'description': 'Изучение русского языка, его грамматики и лексики.',
             'demo_version': 'https://example.com/demo/russian'},
            {'name': 'Литература', 'description': 'Изучение литературы, литературных произведений и их анализ.',
             'demo_version': 'https://example.com/demo/literature'},
            {'name': 'Английский язык', 'description': 'Изучение английского языка как иностранного.',
             'demo_version': 'https://example.com/demo/english'},
            {'name': 'Испанский язык', 'description': 'Изучение испанского языка.',
             'demo_version': 'https://example.com/demo/spanish'},
            {'name': 'Китайский язык', 'description': 'Изучение китайского языка.',
             'demo_version': 'https://example.com/demo/chinese'},
            {'name': 'Немецкий язык', 'description': 'Изучение немецкого языка.',
             'demo_version': 'https://example.com/demo/german'},
            {'name': 'Французский язык', 'description': 'Изучение французского языка.',
             'demo_version': 'https://example.com/demo/french'},
            {'name': 'Искусство', 'description': 'Изучение искусства, художественного творчества.',
             'demo_version': 'https://example.com/demo/art'}
        ],
        'Технические науки': [
            {'name': 'Информатика', 'description': 'Изучение алгоритмов, программирования и технологий.',
             'demo_version': 'https://example.com/demo/computer-science'},
            {'name': 'Технология', 'description': 'Изучение различных технологий и процессов их применения.',
             'demo_version': 'https://example.com/demo/technology'}
        ],
        'Спортивное направление': [
            {'name': 'Физическая культура', 'description': 'Изучение физической активности и её влияния на здоровье.',
             'demo_version': 'https://example.com/demo/sports'}
        ],

        # Подкатегории для каждого направления
        'Математика': [
            {'name': 'Геометрия', 'description': 'Изучение форм и свойств геометрических фигур.',
             'demo_version': 'https://example.com/demo/geometry'},
            {'name': 'Алгебра', 'description': 'Изучение алгебраических выражений и операций.',
             'demo_version': 'https://example.com/demo/algebra'},
            {'name': 'Анализ', 'description': 'Изучение изменений и предельных процессов.',
             'demo_version': 'https://example.com/demo/calculus'},
            {'name': 'Теория чисел', 'description': 'Изучение свойств чисел и их взаимосвязей.',
             'demo_version': 'https://example.com/demo/number-theory'}
        ],
        'Физика': [
            {'name': 'Механика', 'description': 'Изучение движений тел и взаимодействий между ними.',
             'demo_version': 'https://example.com/demo/mechanics'},
            {'name': 'Электродинамика', 'description': 'Изучение электрических и магнитных полей.',
             'demo_version': 'https://example.com/demo/electrodynamics'},
            {'name': 'Оптика', 'description': 'Изучение света, его распространения и взаимодействия.',
             'demo_version': 'https://example.com/demo/optics'},
            {'name': 'Термодинамика', 'description': 'Изучение тепловых процессов и их связи с работой.',
             'demo_version': 'https://example.com/demo/thermodynamics'}
        ],
        'Информатика': [
            {'name': 'Программирование', 'description': 'Изучение основ программирования и разработки ПО.',
             'demo_version': 'https://example.com/demo/programming'},
            {'name': 'Алгоритмы и структуры данных', 'description': 'Изучение эффективных алгоритмов и структур данных.',
             'demo_version': 'https://example.com/demo/algorithms'},
            {'name': 'Искусственный интеллект', 'description': 'Изучение методов создания интеллектуальных систем.',
             'demo_version': 'https://example.com/demo/ai'},
            {'name': 'Компьютерная безопасность', 'description': 'Изучение защиты информации и систем.',
             'demo_version': 'https://example.com/demo/cybersecurity'}
        ],
        'Химия': [
            {'name': 'Органическая химия', 'description': 'Изучение углеродсодержащих соединений.',
             'demo_version': 'https://example.com/demo/organic-chemistry'},
            {'name': 'Неорганическая химия', 'description': 'Изучение всех элементов, кроме углерода.',
             'demo_version': 'https://example.com/demo/inorganic-chemistry'},
            {'name': 'Физическая химия', 'description': 'Изучение физико-химических процессов.',
             'demo_version': 'https://example.com/demo/physical-chemistry'}
        ],
        'Биология': [
            {'name': 'Экология', 'description': 'Изучение взаимодействий живых существ с окружающей средой.',
             'demo_version': 'https://example.com/demo/ecology'},
            {'name': 'Генетика', 'description': 'Изучение наследственности и изменений в генах.',
             'demo_version': 'https://example.com/demo/genetics'},
            {'name': 'Молекулярная биология', 'description': 'Изучение молекул, составляющих живые организмы.',
             'demo_version': 'https://example.com/demo/molecular-biology'}
        ]
    }

    # Создание приложения и контекста
    app = create_app()
    
    with app.app_context():
        # Перебираем направления и добавляем предметы
        for direction_name, subject_list in subjects_data.items():
            direction = Direction.query.filter_by(name=direction_name).first()
            if direction:
                for subject_data in subject_list:
                    subject_name = subject_data['name']
                    description = subject_data['description']
                    demo_version = subject_data['demo_version']
                    
                    # Добавление предмета в базу данных
                    subject = Subject(name=subject_name, description=description, demo_version=demo_version, direction_id=direction.id)
                    db.session.add(subject)
        
        # Сохраняем изменения в базе данных
        db.session.commit()

# Запуск функции
if __name__ == "__main__":
    add_subjects()

# TODO: Заметки
## Автор: Дуплей Максим Игоревич
## Дата: 08.12.2024
