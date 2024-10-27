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
            User(email='ivan@example.com', phone_number='+7-900-123-45-67',
                 photo='static/images/profile_pics/super-cat.jpg', role='student'),
            User(email='maria@example.com', phone_number='+7-900-765-43-21',
                 photo='static/images/profile_pics/super-cat.jpg', role='student'),
            User(email='alexey@example.com', phone_number='+7-900-987-65-43',
                 photo='static/images/profile_pics/super-cat.jpg', role='student'),
        ]

        # Установка паролей
        for user in users:
            user.set_password('123')  # Установите одинаковый пароль для всех пользователей

        # Добавление пользователей в сессию
        db.session.add_all(users)
        db.session.commit()

        # Создание студентов
        students = [
            Student(student_name='Иван', student_surname='Иванов', student_patronymic='Иванович',
                    grade='10', email='ivan@example.com', phone_number='+7-900-123-45-67',
                    photo='static/images/profile_pics/super-cat.jpg', bio = "Пример биографии 1", user_id=users[0].id),
            Student(student_name='Мария', student_surname='Петрова', student_patronymic='Сергеевна',
                    grade='11', email='maria@example.com', phone_number='+7-900-765-43-21',
                    photo='static/images/profile_pics/super-cat.jpg', bio = "Пример биографии 2", user_id=users[1].id),
            Student(student_name='Алексей', student_surname='Сидоров', student_patronymic='Александрович',
                    grade='9', email='alexey@example.com', phone_number='+7-900-987-65-43',
                    photo='static/images/profile_pics/super-cat.jpg', bio = "Пример биографии 3", user_id=users[2].id),
        ]
        
        # Добавление студентов в сессию
        db.session.add_all(students)
        db.session.commit()
        
        # Создание результатов
        results = [
            Result(user_id=users[0].id, score=85, olympiad_name='Олимпиада по математике', date=datetime(2024, 5, 10)),
            Result(user_id=users[1].id, score=90, olympiad_name='Олимпиада по физике', date=datetime(2024, 5, 15)),
            Result(user_id=users[2].id, score=78, olympiad_name='Олимпиада по информатике', date=datetime(2024, 5, 20)),
        ]

        # Добавление результатов в сессию
        db.session.add_all(results)
        db.session.commit()
        
        print("База данных успешно заполнена начальными записями.")

if __name__ == '__main__':
    populate_db()
