from flask import render_template, redirect, url_for, flash
from app.forms.student_form import StudentForm
from app.models.student import Student
from app.extensions import db

def init_routes(app):
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/student', methods=['GET', 'POST'])
    def student():
        form = StudentForm()
        if form.validate_on_submit():
            student = Student(name=form.name.data, score=form.score.data)
            db.session.add(student)
            db.session.commit()
            flash('Student successfully registered!', 'success')
            return redirect(url_for('results'))
        return render_template('student.html', form=form)
    
    @app.route('/results')
    def results():
        students = Student.query.all()
        return render_template('results.html', students=students)
    
    @app.route('/login')
    def login():
        return render_template('login.html')
