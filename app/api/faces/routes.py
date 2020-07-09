from bson.errors import InvalidId
from flask import make_response, jsonify
from flask_restplus import Resource
from werkzeug.utils import secure_filename

from ..authorizations import token_required
from .. import parsers
from . import ns, model, comparison_model
from .controllers import FaceController


#---------------------------------------------
#   DEAL WITH MANY FACES
#---------------------------------------------

@ns.route('/', strict_slashes = False)     # strict_slashes setted to False so the debuger ignores it
@ns.response(404, 'faces not found')
class FaceList(Resource):

    @ns.doc('get_all_faces')
    @ns.response(200, 'success')
    @ns.marshal_list_with(model)
    @token_required
    def get(self):
        """ Get all stored faces data
        """
        return FaceController.getAll(), 200

    @ns.doc('save_many_faces')
    @ns.response(201, 'faces successfuly saved')
    @ns.expect([model])
    @token_required
    def post(self):
        """ Save many faces data
        """
        return make_response(jsonify(FaceController.save_many(ns.payload)), 201)


#---------------------------------------------
#   ENCODINGS
#---------------------------------------------
@ns.route('/encodings', strict_slashes = False)
@ns.response(404, 'not found')
@ns.response(200, 'success')
class FaceEncodings(Resource):

    @ns.doc('get_all_face_encodings')
    @token_required
    def get(self):
        """ Get all stored face encodings
        """
        return make_response(jsonify(FaceController.getAllEncodings()), 200)

    @ns.doc('get_by_encoding')
    @ns.marshal_with(model)
    @token_required
    def post(self):
        """ Get a face document by its encoding
        """
        return FaceController.getByEncoding(ns.payload), 200


#---------------------------------------------
#   NAMES
#---------------------------------------------
@ns.route('/names', strict_slashes = False)
@ns.response(404, 'not found')
@ns.response(200, 'success')
class FaceNameList(Resource):

    @ns.doc('get_all_face_names')
    @token_required
    def get(self):
        """ Get all known face names
        """
        return make_response(jsonify(FaceController.getAllNames()), 200)


#---------------------------------------------
#   FACE DETECTION ROUTING
#---------------------------------------------

@ns.route('/upload/detection', strict_slashes = False)
@ns.response(404, 'upload failed')
@ns.response(200, 'img successfuly uploaded and processed')
class FaceDetection(Resource):

    @ns.doc('detect_faces')
    @ns.expect(parsers.my_parser)
    @token_required
    def post(self):
        """ Upload an image file and detect all faces contained in it
        """
        args = parsers.my_parser.parse_args()
        return make_response(jsonify(FaceController.getEncoding(args['img'])), 200)


#---------------------------------------------
#   FACE RECOGNITION ROUTING
#---------------------------------------------

@ns.route('/upload/recognition', strict_slashes = False)
@ns.response(404, 'upload failed')
@ns.response(200, 'img successfuly uploaded and processed')
class FaceRecognition(Resource):
    
    @ns.doc('recognize_faces')
    @ns.expect(parsers.my_parser)
    @ns.marshal_with(model)
    @token_required
    def post(self):
        """ Upload an image file, detect and attempt to recognize all faces contained in it
        """
        args = parsers.my_parser.parse_args()
        return FaceController.classifyFace(args['img']), 200


@ns.route('/face_match/<float:tolerance>', strict_slashes = False)
@ns.param('tolerance', 'tolerance value for faces comparison')
@ns.response(404, 'not found')
@ns.response(200, 'success')
class FaceMatch(Resource):
    
    @ns.doc('match_faces')
    @ns.expect(comparison_model)
    @token_required
    def post(self, tolerance):
        """ Determines if two faces match according to a tolerance value
        """
        payload = ns.payload
        return make_response(jsonify(FaceController.compareFaces(payload['img1_enc'], payload['img2_enc'], tolerance)), 200)