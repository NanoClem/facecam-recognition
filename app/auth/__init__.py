from flask import Blueprint
import os

from app import base_template_path, base_static_path
from ..extensions import login_manager
from .models import User


# TEMPLATES AND STATIC PATHS
templates_path = os.path.join(base_template_path, 'auth')
static_path    = base_static_path   #os.path.join(base_static_path, 'auth')


# LOGIN BLUEPRINT
login_blueprint = Blueprint('login',  __name__,
                           template_folder=templates_path,
                           static_folder=static_path)

# LOGOUT BLUEPRINT
logout_blueprint = Blueprint('logout',  __name__,
                           static_folder=static_path)

# REGISTER BLUEPRINT
register_blueprint = Blueprint('register',  __name__,
                           template_folder=templates_path,
                           static_folder=static_path)

# CONFIGURE LOGIN MANAGER
login_manager.login_view = 'login.login'
login_manager.login_message = u'You need to be logged in to access this page'

@login_manager.user_loader
def load_user(user_id):
    user = User.getByEmail(user_id)
    return User(user['email']) if user else None


# INIT APP
def init_app(app):
    app.register_blueprint(login_blueprint, url_prefix='/login')
    app.register_blueprint(logout_blueprint, url_prefix='/logout')
    app.register_blueprint(register_blueprint, url_prefix='/register')


from .routes import *