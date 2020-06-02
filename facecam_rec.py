from PIL import Image
import face_recognition
import os


def getImgFiles(foldPath: str, extensions: tuple) -> list:
    """Get every files in folder, filtered with the wanted extensions
    
    Parameters
    -----
        foldPath (str) -- path of the folder where your 
        extensions (list) -- [description]

    Raises
    -----
        OSError -- folder not found
    
    Returns
    -----
        list -- A list of image filenames
    """
    if os.path.isdir(foldPath):
        ret = [f for f in os.listdir(foldPath) if os.path.isfile(os.path.join(foldPath, f)) and f.endswith(extensions)]
    else:
        raise OSError("directory not found")

    return ret


dirpath  = os.getcwd()
datasets = os.path.join(dirpath, 'datasets')
imgs = getImgFiles(datasets, ('.jpg', '.jpeg', '.png'))

image = face_recognition.load_image_file(os.path.join(datasets, imgs[0]))
face_locations = face_recognition.face_locations(image)

for face in face_locations:
    top, right, bottom, left = face
    face_img = image[top:bottom, left:right]
    output = Image.fromarray(face_img)
    output.show()