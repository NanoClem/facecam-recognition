from flask import Blueprint
from flask_restplus import Api


# API blueprint
api_blueprint = Blueprint('api', __name__)

# API constructor
api = Api(api_blueprint,
          title = "Face recognition API",
          description = "Interact with face data services",
          version = 1.0)


def init_app(app):
    """Setup api modules and settings
    
    Parameters
    -----
        app (Flask) -- Flask app object
    """
    from . import users, faces

    # register api namespaces
    users.init_api(api)
    faces.init_api(api)

    # register blueprints
    app.register_blueprint(api_blueprint, url_prefix='/api')