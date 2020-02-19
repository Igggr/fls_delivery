from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email


class AuthForm(FlaskForm):
    mail = EmailField("Электропочта",
                       validators=[InputRequired(), Email()],
                       render_kw={'autofocus': True})
    password = PasswordField("Пароль",
                             validators=[InputRequired()])
    button_text = "Войти"


class RegistrationForm(AuthForm):
    name = StringField("Имя",
                       validators=[InputRequired("""Аноноимусов запретили
                       Пожалуйста введите ваше имя.""")])
    address = StringField("Адресс",
                          validators=[InputRequired("И куда доставлять прикажете?")])
    button_text = "Регистрация"

