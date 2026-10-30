from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, TextAreaField, DecimalField,
                     SelectField, IntegerField, SubmitField)
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange

CATEGORIES = [("electronics", "Електроніка"), ("clothes", "Одяг"),
              ("books", "Книги"), ("other", "Інше")]


class ProductForm(FlaskForm):
    name = StringField("Назва", validators=[
        DataRequired(message="Обов'язкове поле"),
        Length(min=3, message="Мінімум 3 символи")])
    content = TextAreaField("Опис", render_kw={"rows": 5, "cols": 40})
    price = DecimalField("Ціна", places=2, validators=[
        InputRequired(message="Обов'язкове поле"),
        NumberRange(min=0.01, message="Ціна має бути більшою за 0")])
    category = SelectField("Категорія", choices=CATEGORIES)
    quantity = IntegerField("Кількість", validators=[
        InputRequired(message="Обов'язкове поле"),
        NumberRange(min=0, message="Не може бути від'ємною")])
    image = FileField("Зображення", validators=[
        FileAllowed(["png", "jpg", "jpeg"], "Лише PNG, JPG, JPEG")])
    submit = SubmitField("Зберегти")


class DeleteForm(FlaskForm): 
    submit = SubmitField("Видалити")