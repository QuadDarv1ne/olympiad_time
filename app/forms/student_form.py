from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, NumberRange
    
class StudentForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(min=2, max=30)])
    surname = StringField('Фамилия', validators=[DataRequired(), Length(min=2, max=30)])
    patronymic = StringField('Отчество', validators=[Length(max=30)])
    grade = StringField('Класс', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Телефон', validators=[Length(max=15)])
    score = IntegerField('Оценка', validators=[DataRequired(), NumberRange(min=0, max=100)])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
