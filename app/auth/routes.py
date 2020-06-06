from flask import render_template

from ..auth import auth_blueprint as bp


@bp.route('/')
def login():
    """Login page view of the app
    """
    return render_template('login.html', title='Login')