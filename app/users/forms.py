from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, ValidationError, Regexp
)

from app import db
from .models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=14),
        Regexp(
            r'^[A-Za-z][A-Za-z0-9_.]*$',
            message="Username must start with a letter and contain only "
                    "letters, numbers, dots or underscores.",
        ),
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Register now')

    def validate_username(self, username):
        user = db.session.scalar(
            db.select(User).where(User.username == username.data)
        )
        if user:
            raise ValidationError('Користувач з таким username вже існує.')

    def validate_email(self, email):
        user = db.session.scalar(
            db.select(User).where(User.email == email.data)
        )
        if user:
            raise ValidationError(
                f'Користувач з таким емейлом {email.data} вже існує.'
            )