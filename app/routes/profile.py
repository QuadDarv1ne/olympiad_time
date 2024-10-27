# routes/profile.py
import os
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.db.models import Student, User  # Импортируйте ваши модели
from app.forms import ProfileForm
from app import db  # Импортируйте db для сохранения изменений

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required  # Убедитесь, что пользователь аутентифицирован
def edit_profile():
    student = Student.query.filter_by(user_id=current_user.id).first()  # Получите студента по ID пользователя
    form = ProfileForm(obj=student)  # Заполните форму текущими данными

    if form.validate_on_submit():
        # Обновление данных студента
        student.student_name = form.student_name.data
        student.student_surname = form.student_surname.data
        student.student_patronymic = form.student_patronymic.data
        student.grade = form.grade.data
        student.email = form.email.data
        student.phone_number = form.phone_number.data
        
        if form.photo.data:
            # Обработка загрузки фото (например, сохранить файл)
            photo_file = form.photo.data
            photo_filename = secure_filename(photo_file.filename)
            photo_file.save(os.path.join('path/to/save', photo_filename))  # Укажите путь сохранения
            student.photo = photo_filename

        db.session.commit()  # Сохранение изменений в базе данных
        flash('Профиль успешно обновлен!', 'success')
        return redirect(url_for('profile.view_profile'))  # Перенаправление на страницу профиля

    return render_template('edit_profile.html', form=form, student=student)
