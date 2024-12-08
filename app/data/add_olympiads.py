# app/data/add_olympiads.py

"""
Скрипт для добавления олимпиад в таблицу 'olympiad'.

Этот скрипт добавляет все олимпиады для различных предметов в базу данных.
Убедитесь, что предметы, которые будут использоваться в олимпиадах, уже добавлены в таблицу 'subject'.
Для выполнения скрипта используйте команду:
    python app/data/add_olympiads.py
"""

import sys
import os
from datetime import datetime
import json

# Устанавливаем путь до корня проекта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import create_app
from app.db import db
from app.db.models import Olympiad, Subject

# Функция для добавления олимпиад
def add_olympiads():
    # Создание приложения и контекста
    app = create_app()
    
    with app.app_context():
        # Получаем все предметы из базы данных
        subjects = Subject.query.all()
        
        # Данные олимпиады для различных предметов
        olympiads_data = [
            # Математика
            {'subject': 'Математика', 'olympiads': [
                {'name': 'Олимпиада по геометрии', 'date': '2024-01-15', 'description': 'Олимпиада по геометрии для школьников', 'passing_score': 50},
                {'name': 'Олимпиада по алгебре', 'date': '2024-02-10', 'description': 'Олимпиада по алгебре для студентов', 'passing_score': 45},
                {'name': 'Олимпиада по анализу', 'date': '2024-03-20', 'description': 'Олимпиада по математическому анализу', 'passing_score': 55},
                {'name': 'Олимпиада по теории чисел', 'date': '2024-04-25', 'description': 'Олимпиада по теории чисел', 'passing_score': 60}
            ]},
            # Физика
            {'subject': 'Физика', 'olympiads': [
                {'name': 'Олимпиада по механике', 'date': '2024-01-20', 'description': 'Олимпиада по механике для старшеклассников', 'passing_score': 50},
                {'name': 'Олимпиада по электродинамике', 'date': '2024-02-15', 'description': 'Олимпиада по электродинамике', 'passing_score': 45},
                {'name': 'Олимпиада по оптике', 'date': '2024-03-10', 'description': 'Олимпиада по оптике для студентов', 'passing_score': 55},
                {'name': 'Олимпиада по термодинамике', 'date': '2024-04-30', 'description': 'Олимпиада по термодинамике', 'passing_score': 60}
            ]},
            # Информатика
            {'subject': 'Информатика', 'olympiads': [
                {'name': 'Олимпиада по программированию', 'date': '2024-02-01', 'description': 'Олимпиада по программированию для школьников', 'passing_score': 60},
                {'name': 'Олимпиада по алгоритмам и структурам данных', 'date': '2024-03-05', 'description': 'Олимпиада по алгоритмам и структурам данных', 'passing_score': 55},
                {'name': 'Олимпиада по искусственному интеллекту', 'date': '2024-04-15', 'description': 'Олимпиада по искусственному интеллекту', 'passing_score': 65},
                {'name': 'Олимпиада по компьютерной безопасности', 'date': '2024-05-10', 'description': 'Олимпиада по компьютерной безопасности', 'passing_score': 70}
            ]},
            # Химия
            {'subject': 'Химия', 'olympiads': [
                {'name': 'Олимпиада по органической химии', 'date': '2024-01-05', 'description': 'Олимпиада по органической химии', 'passing_score': 50},
                {'name': 'Олимпиада по неорганической химии', 'date': '2024-02-12', 'description': 'Олимпиада по неорганической химии', 'passing_score': 45},
                {'name': 'Олимпиада по физической химии', 'date': '2024-03-18', 'description': 'Олимпиада по физической химии', 'passing_score': 55}
            ]},
            # Биология
            {'subject': 'Биология', 'olympiads': [
                {'name': 'Олимпиада по экологии', 'date': '2024-02-01', 'description': 'Олимпиада по экологии для старшеклассников', 'passing_score': 50},
                {'name': 'Олимпиада по генетике', 'date': '2024-03-10', 'description': 'Олимпиада по генетике для студентов', 'passing_score': 55},
                {'name': 'Олимпиада по молекулярной биологии', 'date': '2024-04-15', 'description': 'Олимпиада по молекулярной биологии', 'passing_score': 60}
            ]},
            # Литература
            {'subject': 'Литература', 'olympiads': [
                {'name': 'Олимпиада по русской литературе', 'date': '2024-01-15', 'description': 'Олимпиада по русской литературе', 'passing_score': 50},
                {'name': 'Олимпиада по зарубежной литературе', 'date': '2024-02-20', 'description': 'Олимпиада по зарубежной литературе', 'passing_score': 45},
                {'name': 'Олимпиада по теории литературы', 'date': '2024-03-25', 'description': 'Олимпиада по теории литературы', 'passing_score': 55}
            ]},
            # История
            {'subject': 'История', 'olympiads': [
                {'name': 'Олимпиада по всемирной истории', 'date': '2024-02-05', 'description': 'Олимпиада по всемирной истории', 'passing_score': 50},
                {'name': 'Олимпиада по истории России', 'date': '2024-03-05', 'description': 'Олимпиада по истории России', 'passing_score': 55},
                {'name': 'Олимпиада по археологии', 'date': '2024-04-10', 'description': 'Олимпиада по археологии', 'passing_score': 60}
            ]},
            # Экономика
            {'subject': 'Экономика', 'olympiads': [
                {'name': 'Олимпиада по микроэкономике', 'date': '2024-01-10', 'description': 'Олимпиада по микроэкономике', 'passing_score': 50},
                {'name': 'Олимпиада по макроэкономике', 'date': '2024-02-15', 'description': 'Олимпиада по макроэкономике', 'passing_score': 55},
                {'name': 'Олимпиада по финансовому анализу', 'date': '2024-03-20', 'description': 'Олимпиада по финансовому анализу', 'passing_score': 60}
            ]},
            # География
            {'subject': 'География', 'olympiads': [
                {'name': 'Олимпиада по физической географии', 'date': '2024-02-10', 'description': 'Олимпиада по физической географии', 'passing_score': 50},
                {'name': 'Олимпиада по экономической географии', 'date': '2024-03-05', 'description': 'Олимпиада по экономической географии', 'passing_score': 55},
                {'name': 'Олимпиада по картографии', 'date': '2024-04-20', 'description': 'Олимпиада по картографии', 'passing_score': 60}
            ]},
            # Социальные науки
            {'subject': 'Социальные науки', 'olympiads': [
                {'name': 'Олимпиада по психологии', 'date': '2024-01-20', 'description': 'Олимпиада по психологии для студентов', 'passing_score': 50},
                {'name': 'Олимпиада по социологии', 'date': '2024-02-25', 'description': 'Олимпиада по социологии', 'passing_score': 55},
                {'name': 'Олимпиада по политологии', 'date': '2024-03-30', 'description': 'Олимпиада по политологии', 'passing_score': 60}
            ]}
        ]

        # Сохраняем данные в JSON файл
        with open('olympiads_data.json', 'w', encoding='utf-8') as f:
            json.dump(olympiads_data, f, ensure_ascii=False, indent=4)
        print("Данные олимпиад успешно сохранены в файл olympiads_data.json")

        # Добавление олимпиад в базу данных
        for olympiad_group in olympiads_data:
            # Ищем предмет по имени
            subject = next((sub for sub in subjects if sub.name == olympiad_group['subject']), None)
            if subject:
                for olympiad in olympiad_group['olympiads']:
                    # Создаем олимпиаду
                    olympiad_entry = Olympiad(
                        subject_id=subject.id,
                        name=olympiad['name'],
                        date=datetime.strptime(olympiad['date'], '%Y-%m-%d'),
                        description=olympiad['description'],
                        passing_score=olympiad['passing_score'],
                        status='upcoming'
                    )
                    # Добавляем олимпиаду в сессию
                    db.session.add(olympiad_entry)

        # Сохраняем изменения в базе данных
        db.session.commit()
        print("Все олимпиады успешно добавлены.")

# Запуск функции
if __name__ == "__main__":
    add_olympiads()

# TODO: Заметки
## Автор: Дуплей Максим Игоревич
## Дата: 08.12.2024
