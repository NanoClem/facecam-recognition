from flask_restplus import fields


# USER MODEL
def create_user_model(ns):
    """ Create a model for users
    """
    return ns.model('User', {
        "_id"        : fields.String(description='unique identifier of the frame'),
        "pseudo"     : fields.String(descritpion='pseudo of the user'),
        'avatar'     : fields.Integer(description='avatard img of the user'),
        'email'      : fields.String(description='email of the user'),
        'password'   : fields.String(description='password of the user'),
        'created_at' : fields.String(description='date of creation')
    })