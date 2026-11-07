from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(min=2, max=100)])
    content = StringField('Вміст', validators=[DataRequired()])
    submit = SubmitField('Зберегти')