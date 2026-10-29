from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, Optional

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[
        DataRequired(message="Обов'язкове поле"),
        Length(min=4, max=10, message="Довжина: від 4 до 10 символів")])
    email = StringField("Email", validators=[
        DataRequired(message="Обов'язкове поле"),
        Email(message="Невірний формат email")])
    phone = StringField("Phone", validators=[
        Optional(),
        Regexp(r"^\+380\d{9}$", message="Формат: +380XXXXXXXXX")])
    subject = SelectField("Subject", choices=[
        ("question", "Питання"),
        ("order", "Замовлення"),
        ("complaint", "Скарга"),
        ("other", "Інше")])
    message = TextAreaField("Message", validators=[
        DataRequired(message="Обов'язкове поле"),
        Length(max=500, message="Максимум 500 символів")])
    submit = SubmitField("Send Message")