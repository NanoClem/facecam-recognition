from flask import render_template, redirect, url_for

from ..auth import login_blueprint as lbp
from ..auth import register_blueprint as rbp
from .forms import LoginForm
from .controllers import login_user



@lbp.route('/', methods=['GET', 'POST'])
def login():
    """Login page view of the app
    """
    form = LoginForm()
    if login_user(form):
        return redirect(url_for('home.home'))
    return render_template('login.html', title='Login', form=form)


@rbp.route('/', methods=['GET', 'POST'])
def register():
    """Register page view of the app
    """
    return render_template('register.html', title='Register')