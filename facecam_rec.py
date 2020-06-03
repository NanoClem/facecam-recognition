from PIL import Image, ImageDraw
import numpy as np
import face_recognition
import os


def getImgFiles(foldPath: str, extensions: tuple) -> list:
    """Get every files in folder, filtered with the wanted extensions
    
    Parameters
    -----
        foldPath (str) -- path of the folder where files are
        extensions (tuple) -- file extensions filter

    Raises
    -----
        OSError -- folder not found
    
    Returns
    -----
        list -- A list of filenames
    """
    if os.path.isdir(foldPath):
        ret = [f for f in os.listdir(foldPath) if os.path.isfile(os.path.join(foldPath, f)) and f.endswith(extensions)]
    else:
        raise OSError("directory not found")

    return ret


dirpath  = os.getcwd()
datasets = os.path.join(dirpath, 'datasets')
imgs     = getImgFiles(datasets, ('.jpg', '.jpeg', '.png'))
resizer  = lambda x, y, s: (int(x*s), int(y*s))              # resize any image to s of its size

# load image with pillow
image = Image.open(os.path.join(datasets, imgs[0]))
# image = image.resize(resizer(*image.size, 0.25), Image.ANTIALIAS).convert('RGB')   # resize img to make face recognition faster
data = np.array(image)

# load img with face_recognition
# image = face_recognition.load_image_file(os.path.join(datasets, imgs[0]))
 
face_locations = face_recognition.face_locations(data)
img_cpy = image.copy()

# Draw a box around each faces
draw = ImageDraw.Draw(img_cpy)
for face in face_locations:
    top, right, bottom, left = face
    draw.rectangle( ((left, top), (right, bottom)), outline=(255, 0, 0), width=1 )
    # Create a new image for each face
    # face_img = image[top:bottom, left:right]
    # output = Image.fromarray(face_img)
    # output.show()

del draw
img_cpy = img_cpy.resize(resizer(*img_cpy.size, 2), Image.ANTIALIAS)
img_cpy.show()