# app/data/add_olympiad_stages.py

'''
Скрипт для добавления этапов олимпиады в базу данных.

Этот скрипт добавляет в таблицу 'olympiad_stages' следующие этапы:
1. Участник
2. Победитель
3. Финалист
4. Призёр

Статус этапа ограничен значениями: 'Участник', 'Победитель', 'Финалист', 'Призёр'.

Перед выполнением убедитесь, что создано и настроено приложение Flask и база данных.

Чтобы выполнить скрипт, используйте команду:
    python app/data/add_olympiad_stages.py
'''

import sys
import os

# Устанавливаем путь до корня проекта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import create_app
from app.db import db
from app.db.models import OlympiadStages

# Функция для добавления этапов олимпиады в базу данных
def add_olympiad_stages():
    olympiad_stages = [
        ("Этап 1", "Участник"),
        ("Этап 2", "Победитель"),
        ("Этап 3", "Финалист"),
        ("Этап 4", "Призёр"),
    ]
    
    # Создание приложения и контекста
    app = create_app()
    
    with app.app_context():
        for name, status in olympiad_stages:
            # Проверяем, если такой этап еще нет в базе
            if not OlympiadStages.query.filter_by(name=name, status=status).first():
                olympiad_stage = OlympiadStages(name=name, status=status)
                db.session.add(olympiad_stage)

        db.session.commit()
        print("Этапы олимпиады успешно добавлены в базу данных.")

if __name__ == "__main__":
    add_olympiad_stages()

# TODO: Заметки
## Автор: Дуплей Максим Игоревич
## Дата: 08.12.2024
