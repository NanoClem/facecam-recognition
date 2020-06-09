from flask import Blueprint
import os
from app import base_template_path, base_static_path


templates_path = os.path.join(base_template_path, 'home')
static_path    = os.path.join(base_static_path, 'home')


# BLUEPRINT
home_blueprint = Blueprint('home',  __name__,
                           template_folder= templates_path,
                           static_folder= static_path,
                           static_url_path=static_path)


def init_app(app):
    app.register_blueprint(home_blueprint, url_prefix='/')
    

from .routes import *