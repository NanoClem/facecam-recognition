from flask import Blueprint


# BLUEPRINT
auth_blueprint = Blueprint('auth',  __name__,
                           template_folder='templates',
                           static_folder='static')

from .routes import *