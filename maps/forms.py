"""Form storage for the map module."""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class LocationForm(FlaskForm):
    """Form for adding new marker to the map."""

    coordinates = StringField(
        "Координаты",
        validators=[DataRequired(), Length(min=7, max=100)],
        render_kw={"placeholder": "Формат: 49.9881, 22.2334"},
    )
    # comment = TextAreaField(
    #     "Комментарий",
    #     validators=[Length(min=0, max=50)],
    #     render_kw={"rows": "2", "placeholder": "Важная информация, если есть"},
    # )
    color = SelectField(
        "Событие",
        choices=[
            ("red", "Вручают"),
            ("yellow", "Возможно вручают"),
            ("green", "Никого нет"),
        ],
    )
    submit = SubmitField("Добавить")
