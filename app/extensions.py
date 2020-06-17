from flask_pymongo import PyMongo
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


mongo         = PyMongo()
csrf          = CSRFProtect()
login_manager = LoginManager()
flask_bcrypt  = Bcrypt()