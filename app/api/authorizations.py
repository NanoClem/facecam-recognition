from functools import wraps
from flask import request
from flask_restplus import abort

from ..extensions import mongo


authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}


#---------------------------------------------
#   API KEY
#---------------------------------------------

def token_required(f):
    @wraps(f)
    def wrap_func(*args, **kwargs):
        token = None

        # TOKEN NOT IN HEADERS
        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']
        
        # EMPTY TOKEN
        if not token:
            abort(401, message='API-KEY is missing')

        # WRONG TOKEN
        res = mongo.db.users.find_one({'api_key': token})
        if not res:
            abort(401, message='unknown API-KEY')

        print('User {} requested with token : {}'.format(res['pseudo'], token))
        return f(*args, **kwargs)

    return wrap_func