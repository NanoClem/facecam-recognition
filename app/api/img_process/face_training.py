import os
import json
import numpy as np
import face_recognition as fr



def getEncodedFaces(img_extensions: tuple) -> list:
    """Look through the given img folder and encode all faces 
    contained in each image. Beware, img filenames should tell exactly whose face it is.
    
    Parameters
    -----
        dirPath (str) -- directory where all face imgs are
        img_extensions (tuple) -- img extensions filter
    
    Returns
    -----
        list -- A list of encoded faces data
    """
    BASE_DIR = os.path.dirname(os.path.relpath(__file__))   # directory where this file is
    img_dir  = os.path.join(BASE_DIR, 'face_imgs')          # directory where training imgs are
    data     = []

    for root, dirs, files in os.walk(img_dir):
        for f in files:
            if f.endswith(img_extensions):
                imgPath = os.path.join(root, f)
                face = fr.load_image_file(imgPath)
                encoding = fr.face_encodings(face)[0]
                data.append( {'imgPath': imgPath, 'name': f.replace('_', ' ').split('.')[0], 'encoding': encoding.tolist()} )

    return data



def getUknownEncoding(img: str) -> np.array:
    """Encode one face given the img filename
    
    Parameters
    -----
        img (str) -- image file path
    
    Returns
    -----
        np.array -- The encoding of the face contained in the image
    """
    face = fr.load_image_file(img)
    encoding = fr.face_encodings(face)[0]

    return encoding




# MAIN
if __name__ == "__main__":
    
    trained_data = getEncodedFaces(('jpg', 'jpeg', 'png'))
    print(json.dumps(trained_data, indent=4))
    

    