import os
import json
import requests
import face_recognition as fr

ALLOWED_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif')



def getTrainEncoding(img_path: str) -> list:
    """Detect and encode one face in the given img filename.
    This includes the img to have exactly one face in it. Otherwise, it will not be processed.
    This function is more suited for training of models.
    
    Parameters
    -----
        img (str) -- image file path
    
    Returns
    -----
        list -- List of the face encoding
    """
    encoding = []
    # CHECK IMG EXTENSION
    if img_path.endswith(ALLOWED_EXTENSIONS):
        img       = fr.load_image_file(img_path)
        faces_loc = fr.face_locations(img)
        # ONLY ONE FACE SHOULD BE FOUND
        if len(faces_loc) != 1:
            print("Image {} not suitable for training: {}".format(img_path, "more than 1 face found" if len(faces_loc) > 1 else "no face found"))
        else:
            encoding = fr.face_encodings(face_image=img, known_face_locations=faces_loc)[0].tolist()    # get the first face encoding in the list
        
    return encoding



def trainAll(train_dir: str) -> list:
    """Look through the img folder and encode all faces 
    contained in each image. Beware, each sub folder should tell exactly whose face it is.
    
    Parameters
    -----
        train_dir (str) -- path of the training directory
    
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
            face_encoding = getTrainEncoding(img)
            data.append( {'img': img, 'name': face_dir.replace('_', ' '), 'encoding': face_encoding} )

    return data



# MAIN
# Run this only to train models
if __name__ == "__main__":

    BASE_DIR     = os.path.dirname(os.path.relpath(__file__))   # directory where this file is
    train_dir    = os.path.join(BASE_DIR, 'face_imgs')          # directory where training imgs are
    trained_data = trainAll(train_dir)

    # SAVE TRAINED DATA
    url = 'http://localhost:5000/api/faces'
    res = requests.post(url, json=trained_data)
    print(json.dumps(res.json(), indent=4))

    

    

    