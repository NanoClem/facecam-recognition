from flask import jsonify
from datetime import datetime
from bson.errors import InvalidId

from ...extensions import mongo
from ..faces import ns



class FaceController(object):
    """
    """
    
    @classmethod
    def getAll(cls):
        """ Get all faces data stored in database
        """
        cursor = mongo.db.faces.find({})
        return list(cursor)