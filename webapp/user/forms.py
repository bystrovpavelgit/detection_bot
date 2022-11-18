""" login form """
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """ class LoginForm """
    username = StringField("Имя пользователя",
        validators=[DataRequired()],
        render_kw={"class": "form-control"})
    password = PasswordField("Пароль",
        validators=[DataRequired()],
        render_kw={"class": "form-control"})
    submit = SubmitField("submit", render_kw={"class": "btn btn-primary"})
