from flask import Blueprint
import os

from app import base_template_path, base_static_path
from ..extensions import login_manager


# TEMPLATES AND STATIC PATHS
templates_path = os.path.join(base_template_path, 'auth')
static_path    = base_static_path   #os.path.join(base_static_path, 'auth')


# AUTH BLUEPRINT
auth_blueprint = Blueprint('auth',  __name__,
                           template_folder=templates_path,
                           static_folder=static_path)

# CONFIGURE LOGIN MANAGER
login_manager.login_view = 'auth.login'
login_manager.login_message = u'You need to be logged in to access this page'


# INIT APP
def init_app(app):
    app.register_blueprint(auth_blueprint, url_prefix='/auth')


from .routes import *