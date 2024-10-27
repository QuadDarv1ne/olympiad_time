# app/populate_db.py
from app import create_app
from app.db.database import db
from app.db.models import User, Student, Result
from werkzeug.security import generate_password_hash
from datetime import datetime

app = create_app()

def populate_db():
    with app.app_context():
        # Удаление всех существующих записей для чистоты
        db.drop_all()
        db.create_all()

        # Создание пользователей
        users = [
            User(first_name='Иван', last_name='Иванов', patronymic='Иванович', 
                 grade='10', email='ivan@example.com', phone_number='89001234567',
                 photo='static/images/profiles/super-cat.jpg', password_hash=generate_password_hash('123')),
            User(first_name='Мария', last_name='Петрова', patronymic='Сергеевна',
                 grade='11', email='maria@example.com', phone_number='89007654321',
                 photo='static/images/profiles/super-cat.jpg', password_hash=generate_password_hash('456')),
            User(first_name='Алексей', last_name='Сидоров', patronymic='Александрович',
                 grade='9', email='alexey@example.com', phone_number='89009876543',
                 photo='static/images/profiles/super-cat.jpg', password_hash=generate_password_hash('789')),
        ]

        # Добавление пользователей в сессию
        db.session.add_all(users)
        db.session.commit()

        # Создание студентов
        students = [
            Student(student_name='Иван', student_last_name='Иванов', student_patronymic='Иванович',
                    grade='10', phone_number='89001234567', photo='static/images/profiles/super-cat.jpg',
                    user_id=1),
            Student(student_name='Мария', student_last_name='Петрова', student_patronymic='Сергеевна',
                    grade='11', phone_number='89007654321', photo='static/images/profiles/super-cat.jpg',
                    user_id=2),
            Student(student_name='Алексей', student_last_name='Сидоров', student_patronymic='Александрович',
                    grade='9', phone_number='89009876543', photo='static/images/profiles/super-cat.jpg',
                    user_id=3),
        ]
        
        # Добавление студентов в сессию
        db.session.add_all(students)
        db.session.commit()
        
        # Создание результатов
        results = [
            Result(user_id=1, score=85, olympiad_name='Олимпиада по математике', date=datetime(2024, 5, 10)),
            Result(user_id=2, score=90, olympiad_name='Олимпиада по физике', date=datetime(2024, 5, 15)),
            Result(user_id=3, score=78, olympiad_name='Олимпиада по информатике', date=datetime(2024, 5, 20)),
        ]

        # Добавление результатов в сессию
        db.session.add_all(results)
        db.session.commit()
        
        print("База данных успешно заполнена начальными записями.")

if __name__ == '__main__':
    populate_db()
