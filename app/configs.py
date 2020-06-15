import os
from datetime import datetime
from dotenv import load_dotenv


load_dotenv('.env')


class Config(object):
    
    MONGO_DBNAME = os.environ.get('MONGO_DBNAME')
    MONGO_URI    = os.environ.get('MONGO_URI')

    SECRET_KEY = os.environ.get('SECRET_KEY')
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY')

    DEBUG = True
