import os
import json
from datetime import datetime
from flask import (
    render_template, redirect, url_for, flash, request, jsonify,
    current_app, Flask, send_file, make_response, abort
)
from werkzeug.utils import secure_filename
from app.forms import LoginForm, RegistrationForm, EditProfileForm, OlympiadRegistrationForm
from app.db.models import Account, Result, Student, Olympiad, OlympiadRegistration, Direction, School, Subject, Scores, OlympiadStages
from app.db.database import db
from flask_login import login_user, logout_user, login_required, current_user
from docx import Document
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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
                filename = f"{form.email.data}_{filename}"  # Уникальное имя файла

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
                return redirect(url_for('login'))  # После успешной регистрации перенаправляем на страницу логина

            flash('Недопустимый файл. Пожалуйста, загрузите изображение формата PNG, JPG или GIF.', 'danger')

        return render_template('register.html', form=form)

    @app.route('/forgot_password', methods=['GET', 'POST'])
    def forgot_password():
        if request.method == 'POST':
            # Ваша логика для восстановления пароля
            email = request.form['email']
            # Логика для отправки письма с восстановлением пароля
            flash('Инструкции по восстановлению пароля отправлены на ваш email.')
            return redirect(url_for('login'))
        return render_template('forgot_password.html')
    
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
        # Загружаем данные из базы данных
        olympiads = Olympiad.query.all()
        return render_template('olympiads.html', olympiads=olympiads)

    # Обработка ошибки 404 (не найдено)
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.route('/register_olympiad/<int:olympiad_id>', methods=['POST'])
    @login_required
    def register_olympiad(olympiad_id):
        olympiad = Olympiad.query.get_or_404(olympiad_id)

        # Проверка: уже зарегистрирован ли студент
        existing_registration = OlympiadRegistration.query.filter_by(
            student_id=current_user.id, 
            olympiad_id=olympiad_id
        ).first()

        if existing_registration:
            flash('Вы уже зарегистрированы на эту олимпиаду.', 'info')
            return redirect(url_for('olympiads'))

        # Создаём новую запись о регистрации
        registration = OlympiadRegistration(
            student_id=current_user.id,
            olympiad_id=olympiad_id
        )
        db.session.add(registration)
        db.session.commit()

        flash(f'Вы успешно зарегистрировались на олимпиаду "{olympiad.name}"', 'success')
        return redirect(url_for('olympiads'))

    @app.route('/profile/<int:student_id>')
    @login_required
    def profile(student_id):
        student = Account.query.get(student_id)
        
        if not student:
            flash('Студент не найден', 'danger')
            return redirect(url_for('index'))
        
        # Получение предметов через олимпиады, на которые зарегистрирован студент
        subjects = Subject.query.filter(
            Subject.id.in_(
                [reg.olympiad.subject_id for reg in student.registrations]
            )
        ).all()

        return render_template('profile.html', student=student, subjects=subjects)

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

    @app.route('/generate_certificate')
    def generate_certificate():
        student = {"student_name": "Иван", "student_surname": "Иванов"}
        olympiad_name = "Математическая олимпиада"
        date = datetime.now().strftime('%d.%m.%Y')
        return render_template('certificate.html', student=student, olympiad_name=olympiad_name, date=date)

    @app.route('/download_certificate')
    def download_certificate():
        # Генерация сертификата с помощью ReportLab
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        c.setFont("Helvetica", 12)

        c.drawString(100, 750, "Сертификат участника")
        c.drawString(100, 730, "Настоящим подтверждается, что Иван Иванов")
        c.drawString(100, 710, "принял(а) участие в мероприятии 'Математическая олимпиада'")
        c.drawString(100, 690, "Дата проведения: 10 января 2025 года")

        c.showPage()
        c.save()

        pdf_buffer.seek(0)
        response = make_response(pdf_buffer.read())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=certificate.pdf'
        return response

    @app.route('/download_certificate_word')
    def download_certificate_word():
        doc = Document()
        doc.add_heading('Сертификат участника', level=1)
        doc.add_paragraph('Настоящим подтверждается, что Иван Иванов')
        doc.add_paragraph('принял(а) участие в мероприятии "Математическая олимпиада".')
        doc.add_paragraph('Дата проведения: 10 января 2025 года')
        doc.add_paragraph('\nРуководитель проекта\n\n___________________')

        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name="certificate.docx",
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    # Обработка ошибок 404
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404
    