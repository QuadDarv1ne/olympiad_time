# routes/profile.py
import os
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.db.models import Account  # Импортируем модель Account
from app.forms import ProfileForm
from app import db  # Импортируем db для сохранения изменений
from werkzeug.utils import secure_filename

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required  # Убедитесь, что пользователь аутентифицирован
def edit_profile():
    account = Account.query.filter_by(id=current_user.id).first()  # Получаем аккаунт пользователя
    form = ProfileForm(obj=account)  # Заполняем форму текущими данными из аккаунта

    if form.validate_on_submit():
        # Обновляем данные аккаунта
        account.email = form.email.data
        account.phone_number = form.phone_number.data
        account.role = form.role.data  # Если форма позволяет изменять роль пользователя (например, student)

        if form.photo.data:
            # Обработка загрузки фото
            photo_file = form.photo.data
            photo_filename = secure_filename(photo_file.filename)
            photo_file.save(os.path.join('path/to/save', photo_filename))  # Укажите путь сохранения
            account.photo = photo_filename

        db.session.commit()  # Сохраняем изменения в базе данных
        flash('Профиль успешно обновлен!', 'success')
        return redirect(url_for('profile.view_profile'))  # Перенаправление на страницу профиля

    return render_template('edit_profile.html', form=form, account=account)
