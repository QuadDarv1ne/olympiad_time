# app/data/add_directions.py
'''
    Скрипт для добавления направлений в базу данных.

    Этот скрипт добавляет в таблицу 'directions' следующие направления:
    1. Естественные науки
    2. Общественные науки
    3. Гуманитарные науки
    4. Технические науки
    5. Спортивное направление

    Каждое направление включает описание, которое сохраняется в поле 'description'.
    Перед выполнением убедитесь, что создано и настроено приложение Flask и база данных.

    Чтобы выполнить скрипт, используйте команду: python app/data/add_directions.py
'''
import sys
import os

# Устанавливаем путь до корня проекта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import create_app
from app.db import db
from app.db.models import Direction

# Функция для добавления направлений в базу данных
def add_directions():
    directions = [
        ("Естественные науки", "Наука, которая занимается исследованием природы, физических и химических процессов."),
        ("Общественные науки", "Изучение общества, социальных процессов и человеческого поведения."),
        ("Гуманитарные науки", "Наука, изучающая культуру, философию, историю и язык."),
        ("Технические науки", "Область науки, направленная на изучение и разработку технологий."),
        ("Спортивное направление", "Наука, занимающаяся изучением физических упражнений, тренировок и спортивных достижений.")
    ]
    
    # Создание приложения и контекста
    app = create_app()
    
    with app.app_context():
        for direction_name, description in directions:
            # Проверяем, если такого направления еще нет в базе
            if not Direction.query.filter_by(name=direction_name).first():
                direction = Direction(name=direction_name, description=description)
                db.session.add(direction)

        db.session.commit()
        print("Направления с описаниями успешно добавлены в базу данных.")

if __name__ == "__main__":
    add_directions()

# TODO: Заметки
## Автор: Дуплей Максим Игоревич
## Дата: 08.12.2024
