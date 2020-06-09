from flask import Blueprint
import os
from app import base_template_path, base_static_path


# TEMPLATES AND STATIC PATHS
templates_path = os.path.join(base_template_path, 'auth')
static_path    = base_static_path   #os.path.join(base_static_path, 'auth')


# LOGIN BLUEPRINT
login_blueprint = Blueprint('login',  __name__,
                           template_folder=templates_path,
                           static_folder=static_path)

# REGISTER BLUEPRINT
register_blueprint = Blueprint('register',  __name__,
                           template_folder=templates_path,
                           static_folder=static_path)


def init_app(app):
    app.register_blueprint(login_blueprint, url_prefix='/login')
    app.register_blueprint(register_blueprint, url_prefix='/register')


from .routes import *