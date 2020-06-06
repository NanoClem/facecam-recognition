from flask import Blueprint
from flask_restplus import Api


# API blueprint
api_blueprint = Blueprint('api', __name__)

# API constructor
api = Api(api_blueprint,
          title = "Face cam recognition",
          description = "Interact with face data processed from a security cam",
          version = 1.0
)


# IMPORT NAMESPACES

# ADD NAMESPACES TO API