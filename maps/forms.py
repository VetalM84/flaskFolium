"""Form storage for the map module."""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError


class LocationForm(FlaskForm):
    coordinates = StringField(
        "Координаты",
        validators=[DataRequired()],
        description="Формат: 49.988, -36.2334",
    )
    comment = StringField("Комментарий", validators=[Length(min=0, max=50)])
    color = SelectField("Событие", choices=[("red", "Вручают"), ("green", "Никого нет")])
    submit = SubmitField("Добавить")

    # def validate_coordinates(self, coordinates):
    #     title = Book.query.filter_by(title=title.data).first()
    #     if title:
    #         raise ValidationError('Такая книга уже есть в списке прочитанных.')

    # def validate_comment(self, comment):
    #     title = Book.query.filter_by(title=title.data).first()
    #     if title:
    #         raise ValidationError('Такая книга уже есть в списке прочитанных.')
