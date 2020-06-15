from flask_pymongo import PyMongo
from flask_wtf import CSRFProtect
from flask_login import LoginManager


mongo         = PyMongo()
csrf          = CSRFProtect()
login_manager = LoginManager()