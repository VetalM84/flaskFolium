from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError


class LocationForm(FlaskForm):
    coordinates = StringField('Координаты', validators=[DataRequired()])
    comment = StringField('Комментарий', validators=[Length(min=0, max=50)])
    color = SelectField('Цвет', choices=[('red', 'Красный'), ('green', 'Зеленый')])
    count_green = IntegerField('Количество зеленых', validators=[DataRequired(), NumberRange(min=0, max=20)])
    count_black = IntegerField('Количество черных', validators=[DataRequired(), NumberRange(min=0, max=20)])
    submit = SubmitField('Добавить')

    # def validate_coordinates(self, coordinates):
    #     title = Book.query.filter_by(title=title.data).first()
    #     if title:
    #         raise ValidationError('Такая книга уже есть в списке прочитанных.')

    # def validate_comment(self, comment):
    #     title = Book.query.filter_by(title=title.data).first()
    #     if title:
    #         raise ValidationError('Такая книга уже есть в списке прочитанных.')
