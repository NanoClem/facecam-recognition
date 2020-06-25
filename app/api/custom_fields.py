from flask_restplus import fields
from bson import ObjectId


class ObjectIdField(fields.Raw):
    def format(self, value):
        if isinstance(value, ObjectId):
            return str(value)
        else:
            raise fields.MarshallingError()