from flask import Blueprint
import os
from app import base_template_path, base_static_path


# TEMPLATES AND STATIC PATHS
templates_path = os.path.join(base_template_path, 'dashboard')
static_path    = base_static_path   #os.path.join(base_static_path, 'dashboard')


# BLUEPRINT
dashboard_blueprint = Blueprint('dashboard',  __name__,
                                template_folder=templates_path,
                                static_folder=static_path)


def init_app(app):
    app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')
    

from .routes import *