from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, DataRequired, Email, EqualTo, Length


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
        Email(message='please enter a valid email')])

    password = PasswordField('Password', validators=[
        InputRequired(message='password required'),
        EqualTo('confirm', message='passwords must match')])

    confirm = PasswordField('Confirm password')
    pseudo  = StringField('Pseudo', validators=[InputRequired(message='pseudo required')])
    submit  = SubmitField('Create account')