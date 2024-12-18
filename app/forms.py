from flask_wtf import FlaskForm
from wtforms import DateField, EmailField, StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from flask_wtf.file import FileAllowed, FileRequired

class RegistrationForm(FlaskForm):
    phone = StringField('Телефон', validators=[
        DataRequired(), 
        Regexp(r'^\+?1?\d{9,15}$', message="Введите правильный номер телефона")
    ])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=8, message="Пароль должен содержать минимум 8 символов")
    ])
    confirm_password = PasswordField('Подтвердите пароль', validators=[
        DataRequired(), 
        EqualTo('password', message='Пароли должны совпадать')
    ])
    
    # Поле для загрузки фотографии с валидатором на допустимый тип файла
    photo = FileField('Фотография', validators=[
        FileRequired(), 
        FileAllowed(['jpg', 'jpeg', 'png'], 'Только изображения')
    ])  
    
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
    phone_number = StringField('Телефон', validators=[
        DataRequired(), 
        Regexp(r'^\+?1?\d{9,15}$', message="Введите правильный номер телефона")
    ])
    grade = SelectField('Класс', choices=[
        ('1', '1 класс'), 
        ('2', '2 класс'), 
        ('3', '3 класс'), 
        ('4', '4 класс'), 
        ('5', '5 класс'), 
        ('6', '6 класс'), 
        ('7', '7 класс'), 
        ('8', '8 класс'), 
        ('9', '9 класс'), 
        ('10', '10 класс'), 
        ('11', '11 класс')
    ], validators=[DataRequired()])  
    bio = TextAreaField('Биография')
    photo = FileField('Фотография', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Только изображения!')
    ])  # Сделано необязательным для редактирования
    submit = SubmitField('Сохранить изменения')

class OlympiadRegistrationForm(FlaskForm):
    title = StringField('Название Олимпиады', validators=[DataRequired()])
    date = DateField('Дата Олимпиады', format='%Y-%m-%d', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    image = FileField('Изображение', validators=[
        FileRequired(), 
        FileAllowed(['jpg', 'jpeg', 'png'], 'Только изображения!')
    ])
    submit = SubmitField('Зарегистрировать Олимпиаду')
