from bson.errors import InvalidId
from flask_restplus import Resource

from ..faces import ns, model
from .controllers import FaceController



@ns.route('/many', strict_slashes = False)     # strict_slashes setted to False so the debuger ignores it
@ns.response(404, 'faces not found')
class FaceList(Resource):
    """
    """

    @ns.doc('get_all_faces')
    @ns.response(200, 'Success')
    @ns.marshal_list_with(model)
    def get(self):
        return FaceController.getAll(), 200