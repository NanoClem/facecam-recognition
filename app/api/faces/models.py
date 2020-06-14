from flask_restplus import fields


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
        "_id"          : fields.String(description='unique identifier of the face'),
        "name"         : fields.String(descritpion='name given to the face', default='Unknown'),
        'img'          : fields.Integer(description='img associated with the face'),
        'encoded_face' : fields.List(fields.Float(), description='encoded face in the img'),
        'private'      : fields.Boolean(description='tells if the img containing the face can be displayed publicly or not', default=True),
        'created_at'   : fields.String(description='date of creation')
    })