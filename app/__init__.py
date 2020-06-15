import os
from flask import Flask

from .configs import Config



# PATHS
base_path = os.path.join(os.getcwd(), 'app')
base_template_path = os.path.join(base_path, 'templates')
base_static_path = os.path.join(base_path, 'static')


# FLASK APP FACTORY
def create_app(config_object=Config):
    """Create a new Flask app object
    
    Parameters
    -----
        config_object (module) -- file dedicated to configuration in Flask env (default: settings)
    
    Returns
    -----
        Flask -- Instanciated Flask object with all configurations and app setup 
    """
    from .customs_encoders import ObjectIdConverter, MongoJSONEncoder
    from .extensions import mongo, csrf, login_manager
    from . import api, home, auth, dashboard

    # FLASK APP OBJECT
    app = Flask(__name__)

    # APP CONFIGURATION
    app.config.from_object(config_object)
    app.url_map.converters['objectid'] = ObjectIdConverter
    app.json_encoder = MongoJSONEncoder

    # LOAD EXTENSIONS
    mongo.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    # INIT APP MODULES
    api.init_app(app)
    home.init_app(app)
    auth.init_app(app)
    dashboard.init_app(app)
    
    return app