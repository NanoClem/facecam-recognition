from flask_restplus import fields
from ..custom_fields import ObjectIdField


# FACE MODEL
def create_face_model(ns):
    """Create a model for users
    
    Parameters
    -----
        ns (flask_restplus.Namespace) -- Namespace for faces operation
    Returns
    -----
        flask_restplus.Namespace.model -- resulting faces model
    """
    return ns.model('Face', {
        "_id"        : ObjectIdField(description='unique identifier of the face'),
        "name"       : fields.String(descritpion='name given to the face', default='Unknown'),
        'img'        : fields.Integer(description='img associated with the face'),
        'nb_faces'   : fields.Integer(description='number of faces found in the img'),
        'encoding'   : fields.List(fields.Float(), description='encoded face in the img'),
        'private'    : fields.Boolean(description='tells if the img containing the face can be displayed publicly or not', default=False),
        'created_at' : fields.String(description='date of creation')
    })