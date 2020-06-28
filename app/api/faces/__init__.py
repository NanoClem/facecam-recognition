from flask_restplus import Namespace
import os

from app.extensions import mongo
from .models import create_face_model


# NAMESPACE
ns = Namespace('face', 
                description = 'Faces related operations', 
                endpoint='face')

model = create_face_model(ns)


def init_api(api):
    """Setup api
    
    Parameters
    -----
        api (flask_restplus.Api) -- Flask Api object
    """
    api.add_namespace(ns)


from .routes import *
