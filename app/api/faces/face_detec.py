import os
import json
import numpy as np
import face_recognition as fr




def getEncoding(img, extensions: tuple=()) -> list:
    """Detect and encode one or many faces contained in the given img.
    This function is more suited for an api request.
    
    Parameters
    -----
        img -- image file path or file stream
        extensions (tuple) -- img extensions filter (default : ())
    
    Returns
    -----
        list -- List of encoded faces contained in the image
    """
    encoding = []
    nb_faces = 0

    if not extensions or img.endswith(extensions):
        im = fr.load_image_file(img)
        faces_loc = fr.face_locations(im)
        # CHECK IF AT LEAST ONE FACE IS FOUND
        if len(faces_loc) > 0 :
            nb_faces = len(faces_loc)
            encoding = fr.face_encodings(face_image=img, known_face_locations=faces_loc).tolist()

    return {'img': img, 'nb_faces': nb_faces, 'encoding': encoding}



def getTrainEncoding(img_path: str, extensions: tuple=()) -> list:
    """Detect and encode one face in the given img filename.
    This includes the img to have exactly one face in it. Otherwise, it will not be processed.
    This function is more suited for training of models.
    
    Parameters
    -----
        img (str) -- image file path
        extensions (tuple) -- img extensions filter (default : ())
    
    Returns
    -----
        list -- List of the face encoding
    """
    encoding = []
    # CHECK IMG EXTENSION
    if not extensions or img_path.endswith(extensions):
        img       = fr.load_image_file(img_path)
        faces_loc = fr.face_locations(img)
        # ONLY ONE FACE SHOULD BE FOUND
        if len(faces_loc) != 1:
            print("Image {} not suitable for training: {}".format(img_path, "more than 1 face found" if len(faces_loc) > 1 else "no face found"))
        else:
            encoding = fr.face_encodings(face_image=img, known_face_locations=faces_loc)[0].tolist()    # get the first face encoding in the list
        
    return encoding



def trainAll(train_dir: str, extensions: tuple=()) -> list:
    """Look through the img folder and encode all faces 
    contained in each image. Beware, each sub folder should tell exactly whose face it is.
    
    Parameters
    -----
        train_dir (str) -- path of the training directory
        extensions (tuple) -- img extensions filter (default : ())
    
    Returns
    -----
        list -- A list of encoded faces data
    """
    data = []
    for face_dir in os.listdir(train_dir):
        d = os.path.join(train_dir, face_dir)

        if not os.path.isdir(d):
            continue
        
        for img_path in os.listdir(d):
            img = os.path.join(d, img_path)
            face_encoding = getTrainEncoding(img, extensions)
            data.append( {'imgPath': img, 'name': face_dir.replace('_', ' '), 'encoding': face_encoding} )

    return data



# MAIN
if __name__ == "__main__":

    BASE_DIR     = os.path.dirname(os.path.relpath(__file__))   # directory where this file is
    train_dir    = os.path.join(BASE_DIR, 'face_imgs')          # directory where training imgs are
    trained_data = trainAll(train_dir, ('jpg', 'jpeg', 'png'))
    
    print(json.dumps(trained_data, indent=4))

    

    