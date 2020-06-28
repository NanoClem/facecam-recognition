from flask import jsonify
from flask_login import UserMixin

from datetime import datetime
from bson.errors import InvalidId

from ...extensions import mongo, login_manager
from ..users import ns



class User(UserMixin):
    """
    """

    def __init__(self, email, pseudo, password):
        """
        """
        self.email = email
        self.pseudo = pseudo
        self.password = password

    #---------------------------------------------
    #   USERMIXIN IMPLEMENTATION
    #---------------------------------------------

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email


    def exists(self, data: dict) -> bool:
        """Check if a user already exists in the database collection
        
        Parameters
        -----
            data (dict) -- user data from payload

        Returns
        -----
            bool -- True if the users exists, otherwise False
        """
        return self.db.count_documents(data, limit = 1) != 0

    
    def toJSON(self):
        return {
            'email': self.email,
            'pseudo': self.pseudo,
            'password': self.password
        }


    #---------------------------------------------
    #   GET
    #---------------------------------------------

    @classmethod
    def getAll(cls):
        """ Get all users stored in database 
        """
        cursor = list(mongo.db.users.find({}))
        return cursor


    @classmethod
    def get_user(cls, data):
        """ Get one or many user matching with the payload
        """
        cursor = list(mongo.db.users.find(data))
        return cursor


    @classmethod
    def getByPseudo(cls, pseudo):
        """ Get a user by its pseudo
        """
        data = mongo.db.users.find_one({"pseudo": pseudo})
        if data:
            return data
        return {}


    @classmethod
    def getByEmail(cls, email):
        """ Get a user by its email
        """
        data = mongo.db.users.find_one({"email": email})
        if data:
            return data
        return {}
        

    #---------------------------------------------
    #   POST
    #---------------------------------------------

    @classmethod
    def create_user(cls, data):
        """ Create a new user
        """
        if cls.exists(data):
            ns.abort(409, message="user already exists", data={})

        cpy_data = data
        cpy_data['created_at'] = datetime.now()
        res = mongo.db.users.insert_one(cpy_data)
        return jsonify( {'inserted_id': res.inserted_id} )


    @classmethod
    def createMany(cls, dataList):
        """ Create multiple data documents
        """
        cpy_data = dataList
        for data in dataList:
            if cls.exists(data):   # avoid duplicates
                cpy_data.remove(data)
            else:
                data['created_at'] = datetime.now()
        
        res = mongo.db.users.insert_many(cpy_data)
        return jsonify( {'inserted_ids': res.inserted_ids} )


    #---------------------------------------------
    #   UPDATE
    #---------------------------------------------

    @classmethod
    def updateById(cls, id, data):
        """ Update a user by its id
        """
        try:
            mongo.db.users.update_one({'_id': id}, {'$set': data})
            return ''
        except InvalidId:
            ns.abort(422, message="Invalid id {}".format(id), data={})


    #---------------------------------------------
    #   DELETE
    #---------------------------------------------

    @classmethod
    def deleteById(cls, id):
        """ Delete a user by its id
        """
        try:
            mongo.db.users.delete_one({'_id': id})
            return ''
        except InvalidId:
            ns.abort(422, message="Invalid id {}".format(id), data={})


# USER LOADER
@login_manager.user_loader
def load_user(user_id):
    user = User.getByEmail(user_id)
    return User(
        email=user['email'], 
        pseudo=user['pseudo'], 
        password=user['password'])