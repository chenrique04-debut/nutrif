
from flask_wtf import FlaskForm
from wtforms.fields import StringField, EmailField, PasswordField, SubmitField

class LoginForm(FlaskForm):
  email = EmailField("E-mail")
  password = PasswordField("Senha")
  submit = SubmitField("logar")

class RegisterForm(FlaskForm):
  name = StringField("Nome")
  email = EmailField("E-mail")
  password = PasswordField("Senha")
  submit = SubmitField("cadastrar")