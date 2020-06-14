import os
from datetime import datetime
from dotenv import load_dotenv


load_dotenv('.env')


class Config(object):
    
    # MONGO
    MONGO_DBNAME = os.environ.get('MONGO_DBNAME')
    MONGO_URI    = os.environ.get('MONGO_URI')

    DEBUG = True
