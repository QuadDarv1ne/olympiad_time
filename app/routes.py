import json
import os
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, jsonify
from werkzeug.utils import secure_filename
from app.forms import LoginForm, RegistrationForm
from app.models import Student, User
from app.extensions import db
from flask_login import login_user, logout_user, login_required, current_user

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Загрузка данных из JSON-файла
def load_olympiads():
    with open('olympiads.json', 'r', encoding='utf-8') as f:
        olympiads_data = json.load(f)
        # Преобразуем строки даты в объекты datetime
        for olympiad in olympiads_data:
            olympiad['date'] = datetime.strptime(olympiad['date'], '%Y-%m-%d')
        return olympiads_data
    
def init_routes(app):
    # Настройки для загрузки файлов
    app.config['UPLOAD_FOLDER'] = 'static/images/'
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Допустимые форматы файлов

    # Главная страница
    @app.route('/')
    def index():
        return render_template('index.html')

    # Страница авторизации
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            flash('Вы уже вошли в систему.', 'info')
            return redirect(url_for('index'))

        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы успешно вошли в систему!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('index'))
            else:
                flash('Неправильное имя пользователя или пароль', 'danger')

        return render_template('login.html', form=form)


    # Страница регистрации
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            flash('Вы уже зарегистрированы и вошли в систему.', 'info')
            return redirect(url_for('index'))

        form = RegistrationForm()
        if form.validate_on_submit():
            # Проверка на существующего пользователя
            existing_user = User.query.filter((User.username == form.username.data) | 
                                            (User.email == form.email.data)).first()

            if existing_user:
                flash('Пользователь с таким именем или email уже существует.', 'danger')
                return redirect(url_for('register'))

            # Обработка загрузки фотографии
            if 'photo' not in request.files:
                flash('Нет загруженного файла!', 'danger')
                return redirect(url_for('register'))

            file = request.files['photo']
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Сохранение файла в папку

                # Создание нового пользователя
                new_user = User(
                    username=form.username.data,
                    email=form.email.data,
                    role='student'  # Установка роли пользователя по умолчанию
                )
                new_user.set_password(form.password.data)  # Хеширование пароля
                new_user.photo = filename  # Сохранение имени файла

                db.session.add(new_user)  # Добавление нового пользователя в сессию
                db.session.commit()  # Сохранение изменений в базе данных

                flash('Регистрация прошла успешно. Теперь вы можете войти в систему.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Недопустимый файл. Пожалуйста, загрузите изображение формата PNG, JPG или GIF.', 'danger')

        return render_template('register.html', form=form)

    # Выход из системы
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Вы успешно вышли из системы.', 'success')
        return redirect(url_for('index'))

    # Маршрут для страницы олимпиад
    @app.route('/olympiads')
    def olympiads():
        olympiads = load_olympiads()
        return render_template('olympiads.html', olympiads=olympiads)

    # Обработка ошибки 404 (не найдено)
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.route('/register_olympiad/<int:olympiad_id>', methods=['GET', 'POST'])
    @login_required
    def register_olympiad(olympiad_id):
        olympiads = load_olympiads()
        olympiad = next((o for o in olympiads if o['id'] == olympiad_id), None)

        if olympiad is None:
            flash('Олимпиада не найдена.', 'danger')
            return redirect(url_for('olympiads'))

        if request.method == 'POST':
            # Логика для регистрации на олимпиаду (например, создание связи между пользователем и олимпиадой в БД)
            flash('Вы успешно зарегистрировались на олимпиаду!', 'success')
            return redirect(url_for('olympiads'))

        return render_template('register_olympiad.html', olympiad=olympiad)

