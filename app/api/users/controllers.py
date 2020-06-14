from flask import jsonify
from datetime import datetime
from bson.errors import InvalidId



class UserController(object):
    """
    """

    def __init__(self, database, namespace):
        """
        """
        self.db = database
        self.ns = namespace


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


    #---------------------------------------------
    #   GET
    #---------------------------------------------

    def getAll(self):
        """ Get all users stored in database 
        """
        cursor = list(self.db.find({}))
        return jsonify(cursor)


    def get_user(self, data):
        """ Get one or many user matching with the payload
        """
        cursor = list(self.db.find(data))
        return jsonify(cursor)


    def getByPseudo(self, pseudo):
        """ Get a user by its pseudo
        """
        data = self.db.find_one({"pseudo": pseudo})
        if data:
            return jsonify(data)
        return {}
        

    #---------------------------------------------
    #   POST
    #---------------------------------------------

    def create_user(self, data):
        """ Create a new user
        """
        if self.exists(data):
            self.ns.abort(409, message="user already exists", data={})

        cpy_data = data
        cpy_data['created_at'] = datetime.now()
        res = self.db.insert_one(cpy_data)
        return jsonify( {'inserted_id': res.inserted_id} )


    def createMany(self, dataList):
        """ Create multiple data documents
        """
        cpy_data = dataList
        for data in dataList:
            if self.exists(data):   # avoid duplicates
                cpy_data.remove(data)
            else:
                data['created_at'] = datetime.now()
        
        res = self.db.insert_many(cpy_data)
        return jsonify( {'inserted_ids': res.inserted_ids} )


    #---------------------------------------------
    #   UPDATE
    #---------------------------------------------

    def updateById(self, id, data):
        """ Update a user by its id
        """
        try:
            self.db.update_one({'_id': id}, {'$set': data})
            return ''
        except InvalidId:
            self.ns.abort(422, message="Invalid id {}".format(id), data={})


    #---------------------------------------------
    #   DELETE
    #---------------------------------------------

    def deleteById(self, id):
        """ Delete a user by its id
        """
        try:
            self.db.delete_one({'_id': id})
            return ''
        except InvalidId:
            self.ns.abort(422, message="Invalid id {}".format(id), data={})