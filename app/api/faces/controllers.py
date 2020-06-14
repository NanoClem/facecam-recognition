from flask import jsonify
from datetime import datetime
from bson.errors import InvalidId



class FaceController(object):
    """
    """
    
    def __init__(self, database, namespace):
        """
        """
        self.db = database
        self.ns = namespace