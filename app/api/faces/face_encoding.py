import os
import json
import numpy as np
import face_recognition as fr


def getEncoding(img_path: str, extensions: tuple=()) -> list:
    """Encode all faces in the given img filename
    
    Parameters
    -----
        img (str) -- image file path
        extensions (tuple) -- img extensions filter (default : ())
    
    Returns
    -----
        list -- List of encoded faces contained in the image
    """
    encoding = np.array([])
    # CHECK IMG EXTENSION
    if extensions and img_path.endswith(extensions):
        img       = fr.load_image_file(img_path)
        faces_loc = fr.face_locations(img)
        # ONLY ONE FACE SHOULD BE FOUND
        ## TODO 1 : allow the img to have multiple face
        ## TODO 2 : check if each isn't already known and associate the name if so
        if len(faces_loc) != 1:
            print("Image {} not suitable for training: {}".format(img_path, "more than 1 face found" if len(faces_loc) > 1 else "no face found"))
        else:
            encoding = fr.face_encodings(face_image=img, known_face_locations=faces_loc)[0].tolist()
        

    return encoding



def getAllEncodedFaces(train_dir: str, extensions: tuple=()) -> list:
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
            faces_encoding = getEncoding(img, extensions)
            data.append( {'imgPath': img, 'name': face_dir.replace('_', ' '), 'encoding': faces_encoding} )

    return data



# MAIN
if __name__ == "__main__":

    BASE_DIR     = os.path.dirname(os.path.relpath(__file__))   # directory where this file is
    train_dir    = os.path.join(BASE_DIR, 'face_imgs')          # directory where training imgs are
    trained_data = getAllEncodedFaces(train_dir, ('jpg', 'jpeg', 'png'))
    
    print(json.dumps(trained_data, indent=4))

    

    