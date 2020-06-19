from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, DataRequired, Email, EqualTo, Length, ValidationError

from .models import User


# CUSTOM VALIDATORS
def email_exists(form, field):
    if User.getByEmail(field.data):
        raise ValidationError('email already exists')

def pseudo_exists(form, field):
    if User.getByPseudo(field.data):
        raise ValidationError('pseudo already exists')



# LOGIN
class LoginForm(FlaskForm):

    username = EmailField('Email', validators=[
        InputRequired(message='email required'),
        Length(min=2, max=35), 
        Email(message='enter a valid email')])

    password    = PasswordField('Password', validators=[InputRequired(message='password required')])
    remember_me = BooleanField('remember me')


# REGISTER
class RegisterForm(FlaskForm):

    username = EmailField('Email', validators=[
        InputRequired(message='email required'),
        Length(min=2, max=35), 
        Email(message='please enter a valid email'),
        email_exists])

    password = PasswordField('Password', validators=[
        InputRequired(message='password required'),
        EqualTo('confirm', message='passwords must match')])

    pseudo  = StringField('Pseudo', validators=[
        InputRequired(message='pseudo required'),
        pseudo_exists])

    confirm = PasswordField('Confirm password')
    submit  = SubmitField('Create account')