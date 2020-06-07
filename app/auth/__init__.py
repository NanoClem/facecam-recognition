from flask import Blueprint
import os


static_path = os.path.join(os.path.dirname(os.path.relpath(__file__)), 'static')

# BLUEPRINT
auth_blueprint = Blueprint('auth',  __name__,
                           template_folder='templates',
                           static_folder='static')

from .routes import *