# app/data/add_accounts.py

'''
Скрипт для создания 5 аккаунтов.

Этот скрипт добавляет 5 аккаунтов в таблицу 'account' в базе данных.
Перед выполнением убедитесь, что приложение Flask настроено и база данных подключена.
Чтобы выполнить скрипт, используйте команду:
    python app/data/add_accounts.py
'''

import sys
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

# Устанавливаем путь до корня проекта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import create_app
from app.db import db
from app.db.models import Account

# Функция для создания аккаунтов
def add_accounts():
    # Список данных для 5 аккаунтов
    accounts_data = [
        {'email': 'user1@example.com', 'phone_number': '1234567890', 'password': 'password1', 'role': 'student'},
        {'email': 'user2@example.com', 'phone_number': '1234567891', 'password': 'password2', 'role': 'teacher'},
        {'email': 'user3@example.com', 'phone_number': '1234567892', 'password': 'password3', 'role': 'student'},
        {'email': 'user4@example.com', 'phone_number': '1234567893', 'password': 'password4', 'role': 'admin'},
        {'email': 'user5@example.com', 'phone_number': '1234567894', 'password': 'password5', 'role': 'student'}
    ]

    # Создание приложения и контекста
    app = create_app()
    
    with app.app_context():
        # Перебираем список данных для создания аккаунтов
        for account_data in accounts_data:
            email = account_data['email']
            phone_number = account_data['phone_number']
            password = account_data['password']
            role = account_data['role']
            
            # Создание нового аккаунта
            account = Account(
                email=email,
                phone_number=phone_number,
                role=role,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            account.set_password(password)  # Хешируем пароль перед сохранением

            # Добавление аккаунта в сессию
            db.session.add(account)
        
        # Сохраняем изменения в базе данных
        db.session.commit()
        print("5 аккаунтов успешно добавлены.")

# Запуск функции
if __name__ == "__main__":
    add_accounts()

# TODO: Заметки
## Автор: Дуплей Максим Игоревич
## Дата: 08.12.2024
