from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm, RegistrationForm
from app.db.models import User, Student
from app.db.database import db

def init_routes(app):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.username.data).first()  # Используйте email
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы успешно вошли в систему!', 'success')
                return redirect(url_for('main.index'))
            flash('Неправильное имя пользователя или пароль', 'danger')
        return render_template('login.html', form=form)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))
        form = RegistrationForm()
        
        # Проверяем, существует ли уже пользователь с таким email
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Пользователь с таким email уже существует.', 'danger')
            return render_template('register.html', form=form)

        if form.validate_on_submit():
            # Создание объекта User
            user = User(
                email=form.email.data,
                phone_number=form.phone.data,
                photo=None  # Укажите по умолчанию или обработайте позже
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.flush()  # Чтобы получить id нового пользователя для Student

            # Создание объекта Student
            student = Student(
                student_name=form.name.data,
                student_last_name=form.surname.data,
                student_patronymic=form.patronymic.data,
                grade=form.grade.data,
                email=form.email.data,
                phone_number=form.phone.data,
                photo=None,  # Укажите по умолчанию или обработайте позже
                user_id=user.id  # Связь с пользователем
            )

            db.session.add(student)
            db.session.commit()

            flash('Ваш аккаунт создан! Теперь вы можете войти.', 'success')
            return redirect(url_for('auth.login'))
        
        return render_template('register.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Вы вышли из системы.', 'success')
        return redirect(url_for('main.index'))
