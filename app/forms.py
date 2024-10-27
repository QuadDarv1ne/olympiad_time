from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    phone = StringField('Телефон', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    
    # Поле для загрузки фотографии
    photo = FileField('Фотография', validators=[DataRequired()])  
    
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    username = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class EditProfileForm(FlaskForm):
    student_name = StringField('Имя', validators=[DataRequired()])
    student_surname = StringField('Фамилия', validators=[DataRequired()])
    student_patronymic = StringField('Отчество')
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Телефон', validators=[DataRequired()])
    bio = TextAreaField('Биография')
    photo = FileField('Фотография', validators=[DataRequired()])  
    submit = SubmitField('Сохранить изменения')
    