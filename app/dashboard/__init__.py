from flask import Blueprint


# BLUEPRINT
dashboard_blueprint = Blueprint('dashboard',  __name__,
                                template_folder='templates',
                                static_folder='static')

from .routes import *