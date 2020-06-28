from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user, current_user

from ..auth import auth_blueprint as auth
from .forms import LoginForm, RegisterForm
from .controllers import LoginController, RegisterController
from ..api.users.controllers import User


# LOGIN
@auth.route('/', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Login page view of the app
    """
    # Check if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    
    # Init login form
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        if LoginController.try_login(username, form.password.data):
            user = User.getByEmail(username)
            user_obj = User(user['email'], user['pseudo'], user['password'])
            login_user(user_obj, remember=form.remember_me.data)
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Login Unsuccessful. Wrong email or password', 'danger')
    
    return render_template('login.html', title='Login', form=form)


# LOGOUT
@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    """Logout user and redirection to login
    """
    logout_user()
    return redirect(url_for('auth.login'))


# REGISTER
@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Register page view of the app
    """
    # Check if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
        
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        if RegisterController.register_user(form.username.data, form.pseudo.data, form.password.data):
            return redirect(url_for('auth.login'))
        else:
            flash('Register failed', 'danger')

    return render_template('register.html', title='Register', form=form)