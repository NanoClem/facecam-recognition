from flask_pymongo import PyMongo
from flask_wtf import CSRFProtect

mongo = PyMongo()
csrf  = CSRFProtect()