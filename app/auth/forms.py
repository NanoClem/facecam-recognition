from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length


# LOGIN
class LoginForm(FlaskForm):

    username = EmailField('Email', validators=[
        DataRequired(message='email required'),
        Length(min=2, max=35), 
        Email(message='please enter a valid email')])

    password    = PasswordField('Password', validators=[DataRequired(message='password required')])
    remember_me = BooleanField('remember me')
    submit      = SubmitField('Log in')


# REGISTER
class RegisterForm(FlaskForm):

    username = EmailField('Email', validators=[
        DataRequired(message='email required'),
        Length(min=2, max=35), 
        Email(message='please enter a valid email')])

    password = PasswordField('Password', validators=[
        DataRequired(message='password required'),
        EqualTo('confirm', message='passwords must match')])

    confirm = PasswordField('Confirm password')
    pseudo  = StringField('Pseudo', validators=[DataRequired(message='pseudo required')])
    submit  = SubmitField('Create account')