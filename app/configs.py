import os
from datetime import datetime
from dotenv import load_dotenv


load_dotenv('.env')


class Config(object):
    
    # MONGO
    MONGO_DBNAME = os.environ.get('MONGO_DBNAME')
    MONGO_URI    = os.environ.get('MONGO_URI')

    # KEYS
    SECRET_KEY = os.environ.get('SECRET_KEY')
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY')

    # FLASK BCRYPT
    BCRYPT_LOG_ROUNDS = 12
    BCRYPT_HASH_PREFIX = '2b'

    DEBUG = True
