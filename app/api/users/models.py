from flask_restplus import fields


# USER MODEL
def create_user_model(ns):
    """ Create a model for users
    """
    return ns.model('User', {
        "_id"        : fields.String(description='unique identifier of the frame'),
        "pseudo"     : fields.String(descritpion='pseudo of the user'),
        'avatar'     : fields.String(description='avatard img of the user', default=''),
        'email'      : fields.String(description='email of the user'),
        'password'   : fields.String(description='password of the user'),
        'api_key'    : fields.String(description='api key of the user', default=None),
        'banned'     : fields.Boolean(description='if the user is banned from any service', default=False),
        'admin'      : fields.Boolean(description='if the user has admin rights or not', default=False),
        'created_at' : fields.String(description='date of creation')
    })