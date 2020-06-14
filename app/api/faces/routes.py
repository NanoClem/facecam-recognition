from bson.errors import InvalidId
from flask import make_response
from flask_restplus import Resource

from ..faces import ns, db, ctrl, model



@ns.route('/many', strict_slashes = False)     # strict_slashes setted to False so the debuger ignores it
@ns.response(404, 'faces not found')
class FaceList(Resource):
    """
    """

    @ns.doc('get_all_faces')
    @ns.response(200, 'Success')
    def get(self):
        return make_response(ctrl.getAll(), 200)