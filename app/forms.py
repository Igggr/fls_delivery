from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email


class AuthForm(FlaskForm):
    email = EmailField("Электропочта",
                       validators=[InputRequired(), Email()],
                       render_kw={'autofocus': True})
    password = PasswordField("Пароль",
                             validators=[InputRequired()])


