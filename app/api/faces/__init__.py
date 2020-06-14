from flask_restplus import Namespace

from app.extensions import mongo
from .models import create_face_model
from .controllers import FaceController


# NAMESPACE
ns = Namespace('face', 
                description = 'Faces related operations', 
                endpoint='face')

db    = mongo.db.faces            # db collection
model = create_face_model(ns)     # model
ctrl  = FaceController(db, ns)    # record controller


def init_api(api):
    """Setup api
    
    Parameters
    -----
        api (flask_restplus.Api) -- Flask Api object
    """
    api.add_namespace(ns)


from .routes import *
