import os
import numpy
from flask import jsonify
from datetime import datetime
from bson.errors import InvalidId
import face_recognition as fr
# from werkzeug.utils import secure_filename

from ...extensions import mongo
from ..parsers import my_parser
from ..faces import ns



class FaceController(object):
    """
    """

    ALLOWED_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif')
    UPLOAD_DIR = os.path.join(os.path.dirname(os.path.relpath(__file__)), 'face_imgs')


    @classmethod
    def exists(cls, face_data):
        """ Tells if a face document already exists in database
        """
        return mongo.db.faces.count_documents(face_data, limit=1) != 0


    # @classmethod
    # def upload(cls, name):
    #     """
    #     """
    #     args     = my_parser.parse_args()
    #     upFile   = args['file']
    #     filename = secure_filename(upFile.filename)

    #     if upFile.mimetype == 'application/xls' and filename.endswith(cls.ALLOWED_EXTENSIONS):
    #         filepath = os.path.join(cls.UPLOAD_DIR, filename)
    #         upFile.save(filepath)
    #     else:
    #         ns.abort(400, message='Failed to upload file')
    
    #---------------------------------------------
    #   GET
    #---------------------------------------------

    @classmethod
    def getAll(cls):
        """ Get all faces data stored in database
        """
        cursor = mongo.db.faces.find({})
        return list(cursor)


    #---------------------------------------------
    #   FACE DETECTION
    #---------------------------------------------

    @classmethod
    def getEncoding(cls, img) -> dict:
        """Detect and encode one or many faces contained in the given img.
        This function is more suited for an api request.
        
        Parameters
        -----
            img -- image file stream
        
        Returns
        -----
            list -- List of encoded faces contained in the image
        """
        encoding = []
        nb_faces = 0

        # CHECK IMG EXTENSION
        if img.filename.endswith(cls.ALLOWED_EXTENSIONS):
            im = fr.load_image_file(img)
            faces_loc = fr.face_locations(im)
            # ONE FACE FOUND AT LEAST
            nb_faces = len(faces_loc)
            if nb_faces > 0 :
                encoding = fr.face_encodings(face_image=im, known_face_locations=faces_loc)
                encoding = list(map(list, encoding))    # convert all numpy arrays into list

        return jsonify({'img': img.filename, 'nb_faces': nb_faces, 'encoding': encoding})


    #---------------------------------------------
    #   SAVE DATA
    #---------------------------------------------

    @classmethod
    def save_face(cls, data: dict) -> dict:
        """Save one face in the database
        
        Parameters
        -----
            data (dict) -- face data
        """
        if cls.exists(data):
            ns.abort(409, message="face already exists")

        cpy_data = data
        cpy_data['created_at'] = datetime.now()
        res = mongo.db.faces.insert_one(cpy_data)
        return jsonify( {'inserted_id': res.inserted_id} )