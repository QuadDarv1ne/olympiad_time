from flask import render_template, redirect, url_for, flash, request, session
from app.forms.student_form import StudentForm, LoginForm
from app.models.student import Student
from app.models.student import Olympiad
from app.models.student import Registration
from app.extensions import db
from werkzeug.exceptions import abort

def init_routes(app):
    
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/student', methods=['GET', 'POST'])
    def student():
        form = StudentForm()
        if form.validate_on_submit():
            existing_student = Student.query.filter_by(name=form.name.data).first()
            if existing_student:
                flash('Студент с таким именем уже существует!', 'danger')
            else:
                student = Student(name=form.name.data, score=form.score.data)
                db.session.add(student)
                db.session.commit()
                flash('Студент успешно зарегистрирован!', 'success')
                return redirect(url_for('results'))
        return render_template('student.html', form=form)

    @app.route('/results')
    def results():
        students = Student.query.all()
        if not students:
            flash('Студентов не найдено!', 'warning')
        return render_template('results.html', students=students)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                session['student_id'] = user.id
                flash('Вы успешно вошли в систему!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Неправильное имя пользователя или пароль', 'danger')
        return render_template('login.html', form=form)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.route('/profile/<int:student_id>')
    def profile(student_id):
        student = Student.query.get_or_404(student_id)
        return render_template('profile.html', student=student)

    @app.route('/olympiads')
    def olympiads():
        olympiads = Olympiad.query.all()
        return render_template('olympiads.html', olympiads=olympiads)

    @app.route('/register_olympiad/<int:olympiad_id>')
    def register_olympiad(olympiad_id):
        student_id = session.get('student_id')
        if student_id is None:
            flash('Пожалуйста, войдите в систему, чтобы записаться на олимпиаду.', 'danger')
            return redirect(url_for('login'))

        registration = Registration(student_id=student_id, olympiad_id=olympiad_id)
        db.session.add(registration)
        db.session.commit()
        flash('Вы успешно записаны на олимпиаду!', 'success')
        return redirect(url_for('olympiads'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        # Логика для обработки регистрации
        return render_template('register.html')
