from flask import render_template

from ..dashboard import dashboard_blueprint as bp


@bp.route('/')
def dashboard():
    """Dashboard page view of the app
    """
    return render_template('dashboard.html', title='Dashboard')