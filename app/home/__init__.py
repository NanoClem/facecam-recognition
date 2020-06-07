from flask import Blueprint
import os


static_path = os.path.join(os.path.dirname(os.path.relpath(__file__)), 'static')

# BLUEPRINT
home_blueprint = Blueprint('home',  __name__,
                           template_folder= 'templates',
                           static_folder= 'static',
                           static_url_path=static_path)

from .routes import *