from bson.errors import InvalidId
from flask import make_response
from flask_restplus import Resource

from ..users import ns, model
from .controllers import User



#---------------------------------------------
#   MANY DOCUMENTS
#---------------------------------------------

@ns.route('/many', strict_slashes = False)     # strict_slashes setted to False so the debuger ignores it
@ns.response(404, 'user not found')
class UserList(Resource):
    """ Get a list of all stored users and allows to create many users
    """

    @ns.doc('get_all_users') #, security='apikey')
    @ns.response(200, 'Success')
    @ns.marshal_list_with(model)
    #@token_required
    def get(self):
        """ Return a list of all stored users
        """
        return User.getAll(), 200


    @ns.doc('create_many_users')
    @ns.response(201, 'user successfuly created')
    @ns.expect([model])
    def post(self):
        """ Create many users
        """
        return make_response(User.createMany(ns.payload), 201)


#---------------------------------------------
#   ONE OR MANY DOCUMENT
#---------------------------------------------

@ns.route('/', strict_slashes = False)
@ns.response(404, 'user not found')
class OneUser(Resource):
    """
    """

    @ns.doc('create_one_user')
    @ns.response(201, 'user successfuly created')
    @ns.expect(model)
    def post(self):
        """ Create a new user
        """
        return make_response(User.create_user(ns.payload), 201)


    @ns.doc('get_one_user')
    @ns.response(200, 'Success')
    @ns.expect(model)
    @ns.marshal_list_with(model)
    def get(self):
        """ Get one or many users matching with given body
        """
        return User.get_user(ns.payload), 200


#---------------------------------------------
#   CRUD BY user pseudo
#---------------------------------------------

@ns.route("/<string:pseudo>")
@ns.response(404, 'user not found')
@ns.param('pseudo', 'The user pseudo')
class UserByPseudo(Resource):
    """ Get, update or delete one user by its pseudo
    """

    @ns.doc('get_user_by_pseudo')
    @ns.response(200, 'success')
    @ns.marshal_with(model)
    def get(self, pseudo):
        """ Get a user by its pseudo
        """
        return User.getByPseudo(pseudo), 200


#---------------------------------------------
#   CRUD BY user email
#---------------------------------------------

@ns.route("/<string:email>")
@ns.response(404, 'user not found')
@ns.param('email', 'The user email')
class UserByEmail(Resource):
    """ Get, update or delete one user by its email
    """

    @ns.doc('get_user_by_email')
    @ns.response(200, 'success')
    @ns.marshal_with(model)
    def get(self, email):
        """ Get a user by its email
        """
        return User.getByEmail(email), 200


#---------------------------------------------
#   CRUD BY ID
#---------------------------------------------

@ns.route("/<objectid:id>")
@ns.response(404, 'user not found')
@ns.param('id', 'the user unique identifier')
class UserByID(Resource):
    """ Get, update or delete one user
    """

    @ns.doc('get_user_by_id')
    @ns.response(200, 'Success')
    @ns.marshal_with(model)
    def get(self, id):
        """ Returns a user by its id
        """
        return User.getByID(id), 200


    @ns.doc('delete_user_by_id')
    @ns.response(204, 'user successfuly deleted')
    def delete(self, id):
        """ Delete a user by its id
        """
        return make_response(User.deleteById(id), 204)


    @ns.doc('update_user_by_id')
    @ns.response(204, 'user successfuly updated')
    def put(self, id):
        """ Update a user by its id
        """
        return make_response(User.updateById(id, ns.payload), 204)