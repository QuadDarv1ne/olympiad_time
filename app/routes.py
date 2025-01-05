import logging
import os
import json
import io
from io import BytesIO
from datetime import datetime
from flask import (
    render_template, redirect, url_for, flash, request, jsonify,
    current_app, Flask, send_file, make_response, abort, session
)
from werkzeug.utils import secure_filename
from app.forms import LoginForm, RegistrationForm, EditProfileForm, OlympiadRegistrationForm
from app.db.models import (
    Account, Result, Student, Olympiad, OlympiadRegistration,
    Direction, School, Subject, Scores, OlympiadStages
)
from app.db.database import db
from flask_login import login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from app.db.utils import generate_certificate_full

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Для использования сессий

# Путь к базе данных внутри папки instance
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'instance', 'olympiad_time.db')

# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Проверка разрешённых форматов файлов
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# Загрузка данных олимпиад из JSON-файла
def load_olympiads(filepath='olympiads.json'):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            olympiads_data = json.load(f)
            for olympiad in olympiads_data:
                olympiad['date'] = datetime.strptime(olympiad['date'], '%Y-%m-%d')
            return olympiads_data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        current_app.logger.error(f"Ошибка загрузки олимпиад: {e}")
        return []

# Инициализация маршрутов
def init_routes(app):
    app.config['UPLOAD_FOLDER'] = 'static/images/'
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}


    @app.route('/')
    def index():
        return render_template('index.html')


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
            flash('Неправильное имя пользователя или пароль.', 'danger')

        return render_template('login.html', form=form)


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

            file = request.files.get('photo')
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{form.email.data}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                new_account = Account(email=form.email.data, role='student')
                new_account.set_password(form.password.data)
                new_account.photo = filename

                db.session.add(new_account)
                db.session.commit()

                flash('Регистрация прошла успешно. Теперь вы можете войти в систему.', 'success')
                return redirect(url_for('login'))

            flash('Недопустимый файл. Пожалуйста, загрузите изображение формата PNG, JPG или GIF.', 'danger')

        return render_template('register.html', form=form)


    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Вы успешно вышли из системы.', 'success')
        return redirect(url_for('index'))


    @app.route('/olympiads')
    def olympiads():
        olympiads = Olympiad.query.all()
        return render_template('olympiads.html', olympiads=olympiads)


    @app.route('/register_olympiad/<int:olympiad_id>', methods=['POST'])
    @login_required
    def register_olympiad(olympiad_id):
        olympiad = Olympiad.query.get_or_404(olympiad_id)

        if OlympiadRegistration.query.filter_by(student_id=current_user.id, olympiad_id=olympiad_id).first():
            flash('Вы уже зарегистрированы на эту олимпиаду.', 'info')
        else:
            registration = OlympiadRegistration(student_id=current_user.id, olympiad_id=olympiad_id)
            db.session.add(registration)
            db.session.commit()
            flash(f'Вы успешно зарегистрировались на олимпиаду "{olympiad.name}".', 'success')

        return redirect(url_for('olympiads'))


    @app.route('/profile/<int:student_id>')
    @login_required
    def profile(student_id):
        student = Account.query.get_or_404(student_id)
        subjects = Subject.query.filter(Subject.id.in_([
            reg.olympiad.subject_id for reg in student.registrations
        ])).all()

        return render_template('profile.html', student=student, subjects=subjects)


    @app.route('/profile/edit', methods=['GET', 'POST'])
    @login_required
    def edit_profile():
        form = EditProfileForm()
        if form.validate_on_submit():
            # Обновление данных профиля
            current_user.email = form.email.data
            current_user.phone_number = form.phone_number.data
            
            # Обработка загрузки фото
            if 'photo' in request.files:
                file = request.files['photo']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    unique_filename = f"{current_user.id}_{filename}"  # Уникальное имя файла
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename))
                    current_user.photo = unique_filename

            db.session.commit()
            flash('Профиль успешно обновлен :D', 'success')
            return redirect(url_for('profile', student_id=current_user.id))

        return render_template('edit_profile.html', form=form, student=current_user)


    # Основной маршрут для генерации сертификата
    @app.route('/generate_certificate', methods=['GET', 'POST'])
    def generate_certificate():
        """
        Основной маршрут для генерации сертификата.
        Получает данные через форму или использует статичные значения для теста.
        """
        if request.method == 'POST':
            student_name = request.form['student_name']
            event_name = request.form['event_name']
            event_date = request.form['event_date']
            issuer_name = request.form['issuer_name']
            director_name = request.form['director_name']
            director_position = request.form['director_position']
            methodist_name = request.form['methodist_name']
            methodist_position = request.form['methodist_position']
        else:
            # Статичные значения для теста
            student_name = "Иванову Ивану Ивановичу"
            event_name = "За участие в олимпиаде по математике"
            event_date = "Дата: 08 августа 2024 года"
            issuer_name = "Организация: ОАО \"Наука\""
            director_name = "Дуплей М. И."
            director_position = "Руководитель"
            methodist_name = "Егорова К. П."
            methodist_position = "Главный методист"

        # Сохраняем данные в сессии
        session.update({
            'student_name': student_name,
            'event_name': event_name,
            'event_date': event_date,
            'issuer_name': issuer_name,
            'director_name': director_name,
            'director_position': director_position,
            'methodist_name': methodist_name,
            'methodist_position': methodist_position
        })

        # Генерация сертификата
        certificate_path = generate_certificate_full(
            student_name, event_name, event_date, issuer_name,
            director_name, director_position, methodist_name, methodist_position
        )

        if certificate_path:
            return render_template('certificate.html', **session)

        return "Ошибка при генерации сертификата", 500


    @app.route('/certificate')
    def certificate():
        """
        Страница для просмотра сертификата.
        Получает данные из сессии и передает их в шаблон для отображения.
        """
        return render_template('certificate.html', **session)


    @app.route('/download_certificate')
    def download_certificate():
        """
        Маршрут для скачивания сертификата в формате PDF.
        Генерирует сертификат с данными из сессии и возвращает файл для скачивания.
        """
        pdf_buffer = generate_certificate_full(
            session['student_name'], session['event_name'], session['event_date'],
            session['issuer_name'], session['director_name'], session['director_position'],
            session['methodist_name'], session['methodist_position'], format_type="pdf"
        )
        if pdf_buffer:
            return send_file(pdf_buffer, as_attachment=True, download_name="certificate.pdf", mimetype='application/pdf')
        return "Ошибка при генерации сертификата", 500


    @app.route('/download_certificate_word')
    def download_certificate_word():
        """
        Маршрут для скачивания сертификата в формате Word.
        Генерирует сертификат с данными из сессии и возвращает файл для скачивания.
        """
        word_buffer = generate_certificate_full(
            session['student_name'], session['event_name'], session['event_date'],
            session['issuer_name'], session['director_name'], session['director_position'],
            session['methodist_name'], session['methodist_position'], format_type="docx"
        )
        if word_buffer:
            return send_file(word_buffer, as_attachment=True, download_name="certificate.docx", mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        return "Ошибка при генерации сертификата", 500


    # Маршрут для скачивания сертификата
    @app.route('/download_certificate_image')
    def download_certificate_image():
        """
        Маршрут для скачивания сертификата в выбранном формате (PNG, JPG, BMP).
        Генерирует сертификат с данными из сессии и возвращает изображение для скачивания.
        """
        format_type = request.args.get('format', 'png').lower()
        logging.debug(f"Requested format: {format_type}")
        
        try:
            # Генерация сертификата
            certificate_path = generate_certificate_full(
                session.get('student_name', 'Иван Иванов'),
                session.get('event_name', 'Олимпиада'),
                session.get('event_date', '2025-01-01'),
                session.get('issuer_name', 'Оргкомитет'),
                session.get('director_name', 'Директор'),
                session.get('director_position', 'Должность директора'),
                session.get('methodist_name', 'Методист'),
                session.get('methodist_position', 'Должность методиста'),
                format_type=format_type
            )
            
            mimetype = {
                "png": "image/png",
                "jpg": "image/jpeg",
                "bmp": "image/bmp"
            }.get(format_type, "image/png")

            return send_file(
                certificate_path,
                as_attachment=True,
                download_name=f"certificate_completed.{format_type}",
                mimetype=mimetype
            )
        except Exception as e:
            logging.error(f"Error generating certificate: {e}")
            return jsonify({"error": str(e)}), 500

    
    @app.route('/forgot_password', methods=['GET', 'POST'])
    def forgot_password():
        return render_template('forgot_password.html')


    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404
