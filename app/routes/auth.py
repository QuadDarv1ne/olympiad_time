from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm, RegistrationForm
from app.db.models import Account, Student
from app.db.database import db

def init_routes(app):
    """
    Инициализация маршрутов для аутентификации и регистрации пользователей.

    - /login: Страница входа.
    - /register: Страница регистрации.
    - /logout: Выход из системы.
    """
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Обработка страницы входа."""
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))
        form = LoginForm()
        if form.validate_on_submit():
            account = Account.query.filter_by(email=form.username.data).first()
            if account and account.check_password(form.password.data):
                login_user(account)
                flash('Вы успешно вошли в систему!', 'success')
                return redirect(url_for('main.index'))
            flash('Неправильное имя пользователя или пароль', 'danger')
        return render_template('login.html', form=form)


    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """Обработка страницы регистрации."""
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))  # Если пользователь уже авторизован, редирект на главную страницу
        
        form = RegistrationForm()

        # Проверка на существование пользователя с таким же email
        existing_account = Account.query.filter_by(email=form.email.data).first()
        if existing_account:
            flash('Пользователь с таким email уже существует.', 'danger')
            return render_template('register.html', form=form)  # Если пользователь уже существует, возвращаем форму с ошибкой

        # Если форма отправлена и прошла валидацию
        if form.validate_on_submit():
            account = Account(
                email=form.email.data,
                phone_number=form.phone.data,
                photo=None
            )
            account.set_password(form.password.data)
            db.session.add(account)
            db.session.flush()  # Для получения id аккаунта

            student = Student(
                student_name=form.name.data,
                student_last_name=form.surname.data,
                student_patronymic=form.patronymic.data,
                grade=form.grade.data,
                email=form.email.data,
                phone_number=form.phone.data,
                photo=None,
                user_id=account.id
            )

            db.session.add(student)
            db.session.commit()

            flash('Ваш аккаунт создан. Теперь вы можете войти.', 'success')
            return redirect(url_for('auth.login'))  # Перенаправляем на страницу логина после успешной регистрации

        # Если форма не прошла валидацию (например, неверно введены данные) или запрос GET
        return render_template('register.html', form=form)  # Возвращаем форму с ошибками


    @app.route('/logout')
    @login_required
    def logout():
        """Обработка выхода из системы."""
        logout_user()
        flash('Вы вышли из системы.', 'success')
        return redirect(url_for('main.index'))
