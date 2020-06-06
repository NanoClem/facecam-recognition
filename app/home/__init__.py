from flask import Blueprint


# BLUEPRINT
home_blueprint = Blueprint('home',  __name__,
                           template_folder='templates',
                           static_folder='static')

from .routes import *