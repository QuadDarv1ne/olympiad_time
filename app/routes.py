import json
import os
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.forms import LoginForm, RegistrationForm, EditProfileForm, OlympiadRegistrationForm
from app.db.models import Account, Result, Student, Olympiad, OlympiadRegistration, Direction, School, Subject, Scores, OlympiadStages
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
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

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
            account = Account.query.filter_by(email=form.username.data).first()
            if account and account.check_password(form.password.data):
                login_user(account)
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
            if Account.query.filter_by(email=form.email.data).first():
                flash('Пользователь с таким email уже существует.', 'danger')
                return redirect(url_for('register'))

            # Обработка загрузки фотографии
            if 'photo' not in request.files:
                flash('Нет загруженного файла!', 'danger')
                return redirect(url_for('register'))

            file = request.files['photo']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Для нового пользователя используем уникальное имя файла (например, с использованием email)
                filename = f"{form.email.data}.{filename}"  # или используйте какое-то другое уникальное значение

                # Путь для сохранения фотографии
                photo_path = os.path.join('app', 'static', 'images', 'profile_pics', filename)
                
                # Сохраняем фотографию
                file.save(photo_path)

                # Создаем нового пользователя
                new_account = Account(email=form.email.data, role='student')
                new_account.set_password(form.password.data)
                new_account.photo = filename  # Сохраняем имя файла в базе данных

                db.session.add(new_account)
                db.session.commit()

                flash('Регистрация прошла успешно. Теперь вы можете войти в систему.', 'success')
                return redirect(url_for('login'))

            flash('Недопустимый файл. Пожалуйста, загрузите изображение формата PNG, JPG или GIF.', 'danger')

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

        form = OlympiadRegistrationForm()

        if form.validate_on_submit():
            # Проверка, зарегистрирован ли уже пользователь на олимпиаду
            registration = OlympiadRegistration.query.filter_by(student_id=current_user.id, olympiad_id=olympiad_id).first()
            if registration:
                flash('Вы уже зарегистрированы на эту олимпиаду!', 'warning')
                return redirect(url_for('olympiads'))

            # Создание новой регистрации
            new_registration = OlympiadRegistration(student_id=current_user.id, olympiad_id=olympiad_id)
            db.session.add(new_registration)
            db.session.commit()

            flash('Вы успешно зарегистрировались на олимпиаду!', 'success')
            return redirect(url_for('olympiads'))

        return render_template('register_olympiad.html', olympiad=olympiad, form=form)

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
        form = EditProfileForm()
        if form.validate_on_submit():
            # Обновление профиля аккаунта
            current_user.email = form.email.data
            if 'photo' in request.files:
                file = request.files['photo']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = f"{current_user.id}_{filename}"  # Уникальное имя файла
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                    current_user.photo = filename

            db.session.commit()
            flash('Профиль успешно обновлен!', 'success')
            return redirect(url_for('profile', student_id=current_user.id))

        return render_template('edit_profile.html', form=form)

    @app.route('/olympiads/list')
    def olympiads_list():
        olympiads = Olympiad.query.all()  # Получаем все олимпиады
        return render_template('olympiads_list.html', olympiads=olympiads)
