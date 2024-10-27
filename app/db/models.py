# app/db/models.py
from app.db.database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Модель пользователя (User)
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)                      # Имя
    last_name = db.Column(db.String(150), nullable=False)                       # Фамилия
    patronymic = db.Column(db.String(150), nullable=True)                       # Отчество
    grade = db.Column(db.String(50), nullable=True)                             # Класс
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)  # Электронная почта
    phone_number = db.Column(db.String(20), nullable=True)                      # Номер телефона
    photo = db.Column(db.String(256), nullable=True)                            # Фото
    password_hash = db.Column(db.String(256), nullable=False)                   # Хеш пароля
    role = db.Column(db.String(50), nullable=False, default='student')          # Роль пользователя
    created_at = db.Column(db.DateTime, default=datetime.utcnow)                # Дата создания

    # Метод для хеширования пароля
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Метод для проверки пароля
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Связь с результатами
    results = db.relationship('Result', backref='user', lazy=True)

    # Представление объекта для отладки
    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'  # Изменено для отображения имени и фамилии

# Модель для результатов (Result)
class Result(db.Model):
    __tablename__ = 'result'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Внешний ключ на пользователя
    score = db.Column(db.Integer, nullable=False)                              # Баллы
    olympiad_name = db.Column(db.String(150), nullable=False)                  # Название олимпиады
    date = db.Column(db.DateTime, default=datetime.utcnow)                     # Дата результата

    # Представление объекта для отладки
    def __repr__(self):
        return f'<Result {self.olympiad_name} - {self.score}>'

# Модель для студентов (Student)
class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(150), nullable=False)                   # Имя студента
    student_last_name = db.Column(db.String(150), nullable=False)              # Фамилия студента
    student_patronymic = db.Column(db.String(150), nullable=True)              # Отчество студента
    grade = db.Column(db.String(50), nullable=True)                            # Класс студента
    phone_number = db.Column(db.String(20), nullable=True)                     # Номер телефона студента
    photo = db.Column(db.String(256), nullable=True)                           # Фото студента
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Внешний ключ на пользователя

    # Связь с пользователем
    user = db.relationship('User', backref=db.backref('students', lazy=True))

    # Представление объекта для отладки
    def __repr__(self):
        return f'<Student {self.student_name} {self.student_last_name}>'
