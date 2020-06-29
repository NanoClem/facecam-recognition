from bson.errors import InvalidId
from flask import make_response
from flask_restplus import Resource
from werkzeug.utils import secure_filename

from .. import parsers
from ..faces import ns, model
from .controllers import FaceController



@ns.route('/', strict_slashes = False)     # strict_slashes setted to False so the debuger ignores it
@ns.response(404, 'faces not found')
class FaceList(Resource):
    """
    """

    @ns.doc('get_all_faces')
    @ns.response(200, 'Success')
    @ns.marshal_list_with(model)
    def get(self):
        return FaceController.getAll(), 200

    # @ns.doc('save_one_face')
    # @ns.response(201, 'Face successfuly saved')
    # @ns.marshal_list_with(model)
    # def post(self):
    #     return FaceController.save_face(), 201


@ns.route('/upload/detection', strict_slashes = False)     # strict_slashes setted to False so the debuger ignores it
@ns.response(404, 'upload failed')
class Face(Resource):

    @ns.doc('upload_an_img')
    @ns.response(201, 'Img successfuly uploaded')
    @ns.expect(parsers.my_parser)
    def post(self):
        args  = parsers.my_parser.parse_args()
        print(args['file'])
        return make_response(FaceController.getEncoding(args['file']), 201)