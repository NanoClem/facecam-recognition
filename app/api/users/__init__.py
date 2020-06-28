from flask_restplus import Namespace

from app.extensions import mongo
from .models import create_user_model


# NAMESPACE
ns = Namespace('user', 
                description = 'Users related operations', 
                endpoint='user')

model = create_user_model(ns)   # api model


def init_api(api):
    """Setup api
    
    Parameters
    -----
        api (flask_restplus.Api) -- Flask Api object
    """
    api.add_namespace(ns)


from .routes import *
