import os
import numpy as np
import json
from flask_restplus.utils import unpack
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
    def _exists(cls, face_data):
        """ Tells if a face document already exists in database
        """
        return mongo.db.faces.count_documents(face_data, limit=1) != 0


    # @classmethod
    # def upload(cls, name):
    #     """
    #     """
    #     args     = my_parser.parse_args()
    #     upFile   = args['img']
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
    def getAll(cls) -> list:
        """ Get all faces data stored in database
        """
        cursor = mongo.db.faces.find({})
        return list(cursor)


    @classmethod
    def getAllEncodings(cls) -> list:
        """ Get all face encodings stored in database
        """
        cursor = mongo.db.faces.find({}, {'encoding': 1, '_id': 0})     # remove default included id field
        res    = list(map(lambda doc : doc['encoding'], list(cursor)))  # mapping all encoding
        return res
        

    @classmethod
    def getAllNames(cls) -> list:
        """ Get all face encodings stored in database
        """
        cursor = mongo.db.faces.distinct('name')
        return cursor


    @classmethod
    def getByEncoding(cls, encoding) -> dict:
        """ Get a face document by its encoding
        """
        data = mongo.db.faces.find_one({'encoding': encoding})
        return data if data else {}


    #---------------------------------------------
    #   SAVE DATA
    #---------------------------------------------

    @classmethod
    def save_face(cls, data: dict) -> dict:
        """Save one face data in the database
        
        Parameters
        -----
            data (dict) -- face data
        """
        if cls._exists(data):
            ns.abort(409, message="face already exists")

        cpy_data = data
        cpy_data['created_at'] = datetime.now()
        res = mongo.db.faces.insert_one(cpy_data)
        return {'inserted_id': res.inserted_id}


    @classmethod
    def save_many(cls, data: list) -> dict:
        """Save many face data all at once in the database
        
        Parameters
        -----
            data (list) -- [description]
        
        Returns
        -----
            dict -- [description]
        """
        cpy_data = data
        for d in cpy_data:
            if cls._exists(d):
                cpy_data.remove(d)
            else:
                d['created_at'] = datetime.now()
        
        res = mongo.db.faces.insert_many(cpy_data)
        return {'nb': len(res.inserted_ids), 'inserted_ids': res.inserted_ids}


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
                encoding = list(map(lambda elem : elem.tolist(), encoding))    # convert all numpy arrays into list

        return {'img': img.filename, 'nb_faces': nb_faces, 'encoding': encoding}


    #---------------------------------------------
    #   FACE RECOGNITION
    #---------------------------------------------

    @classmethod
    def compareFaces(cls, enc1: list, enc2: list, tolerance: float) -> dict:
        """Compares two given face encoding and tells if they match
        according to a tolerance value.
        
        Parameters
        -----
            enc1 (list) -- first face encoding
            enc2 (list) -- second face encoding
            tolerance (float) -- value of tolerance when comparing faces encoding. Lower is more strict.
        
        Returns
        -----
            bool -- True if they match, otherwise False.
        """
        enc1  = np.asarray([enc1], dtype=np.float32)
        match = True if fr.compare_faces(enc1, enc2)[0] else False      # numpy bools can't be serialized
        return {"match": match}



    @classmethod
    def classifyFace(cls, img) -> list:
        """Detects and attempts to recognize each face in the given img.
        A face is recognized with the smallest distance between the computed encoding and stored ones.
        
        Parameters
        -----
            im (str) -- image file stream
        
        Returns
        -----
            list -- data about all recognized faces
        """
        # FACE DETECTION AND ENCODING
        newFaces = cls.getEncoding(img)
        data = []

        if newFaces['nb_faces'] > 0:
            knownFacesEncoding = cls.getAllEncodings()
            knownFacesEncoding = np.asarray(knownFacesEncoding, dtype=np.float32)   # convert into ndarray for face_recognition methods
            
            for face in newFaces['encoding']:
                matches          = fr.compare_faces(knownFacesEncoding, face)   # SEE IF THE FACE IS MATCHING WITH A KNOWN ONE
                faceDistances    = fr.face_distance(knownFacesEncoding, face)   # FIND THE KNOWN FACE WITH THE SMALLEST DISTANCE
                bestMatchIndex   = np.argmin(faceDistances)
                matchingEncoding = matches[bestMatchIndex]
                if matchingEncoding:
                    res = knownFacesEncoding[bestMatchIndex].tolist()
                    data.append(cls.getByEncoding(res))

        return data