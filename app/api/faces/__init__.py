from flask_restplus import Namespace
import os

from app.extensions import mongo
from .models import create_face_model
from .controllers import FaceController



# IMAGES AND TRAINING DIRECTORIES
BASE_DIR = os.path.dirname(os.path.relpath(__file__))
train_dir    = os.path.join(BASE_DIR, 'face_imgs')


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
