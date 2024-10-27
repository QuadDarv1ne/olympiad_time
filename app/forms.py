from flask_wtf import FlaskForm
from wtforms import DateField, EmailField, StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField
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
    phone_number = StringField('Телефон', validators=[DataRequired()])
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
    ], validators=[DataRequired()])  # Добавлено поле выбора класса
    bio = TextAreaField('Биография')
    photo = FileField('Фотография')  # Сделано необязательным для редактирования
    submit = SubmitField('Сохранить изменения')

class OlympiadRegistrationForm(FlaskForm):
    title = StringField('Название Олимпиады', validators=[DataRequired()])
    date = DateField('Дата Олимпиады', format='%Y-%m-%d', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    image = FileField('Изображение', validators=[DataRequired()])
    submit = SubmitField('Зарегистрировать Олимпиаду')
    