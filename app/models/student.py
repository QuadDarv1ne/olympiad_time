from app.extensions import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    patronymic = db.Column(db.String(30), nullable=True)
    grade = db.Column(db.String(10), nullable=False)  # Класс
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=True)  # Телефон
    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Student {self.name} {self.surname}>'

class Olympiad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    participants = db.relationship('Student', secondary='registration', backref='olympiads')

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    olympiad_id = db.Column(db.Integer, db.ForeignKey('olympiad.id'))
