from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

# Модель пользователя (User)
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
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
        return f'<User {self.username}>'

# Модель для результатов (Result)
class Result(db.Model):
    __tablename__ = 'result'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    olympiad_name = db.Column(db.String(150), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Представление объекта для отладки
    def __repr__(self):
        return f'<Result {self.olympiad_name} - {self.score}>'

# Модель для студентов (Student) - при необходимости
class Student(db.Model):
    __tablename__ = 'student'
    
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Связь с пользователем
    user = db.relationship('User', backref=db.backref('students', lazy=True))

    # Представление объекта для отладки
    def __repr__(self):
        return f'<Student {self.student_name}>'
