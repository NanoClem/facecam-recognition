from flask import render_template

from ..auth import login_blueprint as lbp
from ..auth import register_blueprint as rbp



@lbp.route('/')
def login():
    """Login page view of the app
    """
    return render_template('login.html', title='Login')


@rbp.route('/')
def register():
    """Register page view of the app
    """
    return render_template('register.html', title='Register')