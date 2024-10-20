from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class StudentForm(FlaskForm):
    name = StringField('Имя студента', validators=[DataRequired()])
    score = IntegerField('Баллы', validators=[DataRequired()])
    submit = SubmitField('Зарегистрировать')
