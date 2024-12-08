# app/data/add_schools.py

"""
Скрипт для добавления школ в таблицу 'school'.

Этот скрипт добавляет данные о 5 школах в базу данных.
Убедитесь, что база данных настроена и доступна.
Для выполнения скрипта используйте команду:
    python app/data/add_schools.py
"""

import sys
import os

# Устанавливаем путь до корня проекта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import create_app
from app.db import db
from app.db.models import School

# Функция для добавления школ
def add_schools():
    # Создание приложения и контекста
    app = create_app()
    
    with app.app_context():
        # Данные о 5 школах
        schools_data = [
            {'name': 'Школа №1', 'address': 'Улица Ленина, 1', 'phone_number': '+7 123 456 7890', 'email': 'school1@example.com', 'website': 'http://school1.example.com', 'student_capacity': 500, 'established_year': 1990, 'description': 'Основная школа с углубленным изучением математики и физики.'},
            {'name': 'Школа №2', 'address': 'Улица Пушкина, 10', 'phone_number': '+7 234 567 8901', 'email': 'school2@example.com', 'website': 'http://school2.example.com', 'student_capacity': 600, 'established_year': 1995, 'description': 'Школа с сильной гуманитарной направленностью.'},
            {'name': 'Школа №3', 'address': 'Улица Чехова, 20', 'phone_number': '+7 345 678 9012', 'email': 'school3@example.com', 'website': 'http://school3.example.com', 'student_capacity': 400, 'established_year': 2000, 'description': 'Школа с курсами по информатике и робототехнике.'},
            {'name': 'Школа №4', 'address': 'Улица Тимирязева, 5', 'phone_number': '+7 456 789 0123', 'email': 'school4@example.com', 'website': 'http://school4.example.com', 'student_capacity': 700, 'established_year': 1985, 'description': 'Школа с углубленным изучением иностранных языков.'},
            {'name': 'Школа №5', 'address': 'Улица Гоголя, 15', 'phone_number': '+7 567 890 1234', 'email': 'school5@example.com', 'website': 'http://school5.example.com', 'student_capacity': 450, 'established_year': 2010, 'description': 'Современная школа с инновационными методами преподавания.'}
        ]

        # Добавление школ в базу данных
        for school in schools_data:
            school_entry = School(
                name=school['name'],
                address=school['address'],
                phone_number=school['phone_number'],
                email=school['email'],
                website=school['website'],
                student_capacity=school['student_capacity'],
                established_year=school['established_year'],
                description=school['description']
            )
            # Добавляем школу в сессию
            db.session.add(school_entry)

        # Сохраняем изменения в базе данных
        db.session.commit()
        print("Все школы успешно добавлены.")

# Запуск функции
if __name__ == "__main__":
    add_schools()

# TODO: Заметки
## Автор: Дуплей Максим Игоревич
## Дата: 08.12.2024
