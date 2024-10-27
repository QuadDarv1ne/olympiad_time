from app import create_app
from app.extensions import db
from app.db.models import User, Result, Student

# Создание экземпляра приложения
app = create_app()

with app.app_context():
    # Проверка, если база данных пустая, чтобы избежать дублирования
    if User.query.count() == 0:
        # Добавление данных
        # Пример пользователей
        user1 = User(username='ученик1', email='uch1@example.com')
        user1.set_password('пароль123')  # Установите пароль
        user2 = User(username='ученик2', email='uch2@example.com')
        user2.set_password('пароль123')

        # Пример результатов
        result1 = Result(user_id=1, score=95, olympiad_name='Олимпиада по математике')
        result2 = Result(user_id=1, score=85, olympiad_name='Олимпиада по естественным наукам')
        result3 = Result(user_id=2, score=90, olympiad_name='Олимпиада по информатике')

        # Пример студентов
        student1 = Student(student_name='Иван Иванов', user_id=1)
        student2 = Student(student_name='Анна Смирнова', user_id=2)

        # Добавление объектов в сессию
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(result1)
        db.session.add(result2)
        db.session.add(result3)
        db.session.add(student1)
        db.session.add(student2)

        # Сохранение изменений
        db.session.commit()

        print("Данные успешно добавлены в базу данных.")
    else:
        print("База данных уже содержит данные. Добавление пропущено.")
