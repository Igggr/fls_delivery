from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, ValidationError, Length
import phonenumbers


class AuthForm(FlaskForm):
    mail = EmailField("Электропочта",
                       validators=[InputRequired(), Email()],
                       render_kw={'autofocus': True})
    password = PasswordField("Пароль",
                             validators=[InputRequired()])
    button_text = "Войти"


class RegistrationForm(AuthForm):
    name = StringField("Ваше имя",
                       validators=[InputRequired(message="""Аноноимусов запретили
                       Пожалуйста введите ваше имя.""")])
    address = StringField("Адресс",
                          validators=[InputRequired(message="И куда доставлять прикажете?")])
    phone = StringField("Телефон",
                         validators=[InputRequired(message="заполни"),
                                    Length(min=6,
                                    message="должен быть > 5 символов")
                                    ],
                        render_kw={"class": "form-control"}
                        )

    def validate_phone(form, field):
        try:
            input_number = phonenumbers.parse(field.data, 'RU')
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError("Некоректный номер")
        except:
            raise ValidationError("Некоректный номер")

    button_text = "Регистрация"


class CSRForm(FlaskForm):
    """I need only csrf_token"""
    pass
