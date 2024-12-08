# app/data/add_students.py

import sys
import os

# Устанавливаем путь до корня проекта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import create_app
from app.db.database import db
from app.db.models import Student, Account

def add_students():
    # Создаем список из 10 студентов
    students_data = [
        ("Иван", "Иванов", "Иванович", "10", "ivanov@example.com", "+71234567890", "photo1.jpg", "Студент 1", 1),
        ("Мария", "Петрова", "Сергеевна", "9", "petrova@example.com", "+71234567891", "photo2.jpg", "Студент 2", 2),
        ("Алексей", "Смирнов", "Алексеевич", "11", "smirnov@example.com", "+71234567892", "photo3.jpg", "Студент 3", 3),
        ("Елена", "Кузнецова", "Васильевна", "10", "kuznetsova@example.com", "+71234567893", "photo4.jpg", "Студент 4", 4),
        ("Дмитрий", "Попов", "Павлович", "8", "popov@example.com", "+71234567894", "photo5.jpg", "Студент 5", 5),
        ("Ольга", "Сидорова", "Ивановна", "7", "sidorova@example.com", "+71234567895", "photo6.jpg", "Студент 6", 6),
        ("Андрей", "Федоров", "Петрович", "9", "fedorov@example.com", "+71234567896", "photo7.jpg", "Студент 7", 7),
        ("Наталья", "Морозова", "Владимировна", "11", "morozova@example.com", "+71234567897", "photo8.jpg", "Студент 8", 8),
        ("Максим", "Борисов", "Максимович", "10", "borisov@example.com", "+71234567898", "photo9.jpg", "Студент 9", 9),
        ("Анна", "Лебедева", "Юрьевна", "8", "lebedeva@example.com", "+71234567899", "photo10.jpg", "Студент 10", 10),
    ]

    # Создание приложения и контекста
    app = create_app()
    
    with app.app_context():
        # Добавляем студентов в базу данных
        for student_data in students_data:
            student = Student(
                student_name=student_data[0],
                student_surname=student_data[1],
                student_patronymic=student_data[2],
                grade=student_data[3],
                email=student_data[4],
                phone_number=student_data[5],
                photo=student_data[6],
                bio=student_data[7],
                account_id=student_data[8]
            )
            db.session.add(student)

        # Сохраняем изменения в базе данных
        db.session.commit()
        print("10 студентов успешно добавлены :D")

# Запуск функции
if __name__ == "__main__":
    add_students()

# TODO: Заметки
## Автор: Дуплей Максим Игоревич
## Дата: 08.12.2024
