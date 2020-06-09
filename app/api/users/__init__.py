from flask_restplus import Namespace

from app.extensions import mongo
from .models import create_user_model
from .controllers import UserController


# NAMESPACE
ns = Namespace('user', 
                description = 'Users related operations', 
                endpoint='user')

db    = mongo.db.users            # db collection
model = create_user_model(ns)     # model
ctrl  = UserController(db, ns)    # record controller


def init_api(api):
    """Setup api
    
    Parameters
    -----
        api (flask_restplus.Api) -- Flask Api object
    """
    api.add_namespace(ns)


from .routes import *
