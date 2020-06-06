from flask import render_template

from ..home import home_blueprint as bp


@bp.route('/')
@bp.route('/home')
def home():
    """Home page view of the app
    """
    return render_template('home.html', title='Home')