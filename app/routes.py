import json
import os
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.db.models import Student, User
from app.db.database import db
from flask_login import login_user, logout_user, login_required, current_user

# Функция для проверки разрешенных форматов файлов
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# Загрузка данных из JSON-файла
def load_olympiads(filepath='olympiads.json'):
    with open(filepath, 'r', encoding='utf-8') as f:
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
            user = User.query.filter_by(email=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы успешно вошли в систему!', 'success')
                return redirect(request.args.get('next') or url_for('index'))
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
            if User.query.filter_by(email=form.email.data).first():
                flash('Пользователь с таким email уже существует.', 'danger')
                return redirect(url_for('register'))

            # Обработка загрузки фотографии
            if 'photo' not in request.files:
                flash('Нет загруженного файла!', 'danger')
                return redirect(url_for('register'))

            file = request.files['photo']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                new_user = User(email=form.email.data, role='student')
                new_user.set_password(form.password.data)
                new_user.photo = filename

                db.session.add(new_user)
                db.session.commit()

                flash('Регистрация прошла успешно. Теперь вы можете войти в систему.', 'success')
                return redirect(url_for('login'))
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

    @app.route('/profile/<int:student_id>')
    @login_required
    def profile(student_id):
        student = Student.query.get(student_id)
        if not student:
            flash('Студент не найден', 'danger')
            return redirect(url_for('index'))
        return render_template('profile.html', student=student)

    @app.route('/profile/edit', methods=['GET', 'POST'])
    @login_required
    def edit_profile():
        form = EditProfileForm()  # Инициализация формы
        if form.validate_on_submit():
            # Логика для обработки формы
            flash('Профиль успешно обновлен!')
            return redirect(url_for('profile'))  # Перенаправление после успешного обновления

        return render_template('edit_profile.html', form=form)  # Передача формы в шаблон
