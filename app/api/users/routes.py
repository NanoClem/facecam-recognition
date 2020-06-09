from bson.errors import InvalidId
from flask import make_response
from flask_restplus import Resource

from ..users import ns, db, ctrl, model



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
    #@ns.marshal_list_with(model)
    #@token_required
    def get(self):
        """ Return a list of all stored users
        """
        return make_response(ctrl.getAll(), 200)


    @ns.doc('create_many_users')
    @ns.response(201, 'user successfuly created')
    @ns.expect([model])
    def post(self):
        """ Create many users
        """
        return make_response(ctrl.createMany(ns.payload), 201)


#---------------------------------------------
#   ONE OR MANY DOCUMENT
#---------------------------------------------

@ns.route('/', strict_slashes = False)
@ns.response(404, 'user not found')
class User(Resource):
    """
    """

    @ns.doc('create_one_user')
    @ns.response(201, 'user successfuly created')
    @ns.expect(model)
    def post(self):
        """ Create a new user
        """
        return make_response(ctrl.create_user(ns.payload), 201)


    @ns.doc('get_one_user')
    @ns.response(200, 'Success')
    @ns.expect(model)
    def get(self):
        """ Get one or many users matching with given body
        """
        return make_response(ctrl.get_user(ns.payload), 200)


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
    def get(self, pseudo):
        """ Get a user by its pseudo
        """
        return make_response(ctrl.getByPseudo(pseudo), 200)


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
    def get(self, id):
        """ Returns a user by its id
        """
        return make_response(ctrl.getByID(id), 200)


    @ns.doc('delete_user_by_id')
    @ns.response(204, 'user successfuly deleted')
    def delete(self, id):
        """ Delete a user by its id
        """
        return make_response(ctrl.deleteById(id), 204)


    @ns.doc('update_user_by_id')
    @ns.response(204, 'user successfuly updated')
    def put(self, id):
        """ Update a user by its id
        """
        return make_response(ctrl.updateById(id, ns.payload), 204)