from flask import render_template
from flask_login import login_required

from ..dashboard import dashboard_blueprint as bp


@bp.route('/', methods=['GET'])
@login_required
def dashboard():
    """Dashboard page view of the app
    """
    return render_template('dashboard.html', title='Dashboard')