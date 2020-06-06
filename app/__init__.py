from flask import Flask
import app.settings as settings



def create_app(config_object=settings):
    """Create a new Flask app object
    
    Parameters
    -----
        config_object (module) -- file dedicated to configuration in Flask env (default: settings)
    
    Returns
    -----
        Flask -- Instanciated Flask object with all configurations and app setup 
    """
    from .customs_encoders import ObjectIdConverter, MongoJSONEncoder
    from .extensions import mongo
    from .api import api_blueprint
    from .home import home_blueprint
    from .auth import auth_blueprint
    from .dashboard import dashboard_blueprint

    # FLASK APP OBJECT
    app = Flask(__name__)

    # APP CONFIGS
    app.config.from_object(config_object)
    app.url_map.converters['objectid'] = ObjectIdConverter
    app.json_encoder = MongoJSONEncoder

    # LOAD EXTENSIONS
    mongo.init_app(app)

    # REGISTER BLUEPRINTS
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(home_blueprint, url_prefix='/')
    app.register_blueprint(auth_blueprint, url_prefix='/login')
    app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')
    
    return app