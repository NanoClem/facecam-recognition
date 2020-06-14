from PIL import Image, ImageDraw
import numpy as np
import face_recognition as fr
from datetime import datetime
import cv2
import os

from .face_training import getEncodedFaces



def drawLabeledBox(img: np.array, top: int, right: int, bottom: int, left: int, label: str, font: int=cv2.FONT_HERSHEY_DUPLEX, textColor: tuple=(255, 255, 255), thickColor: tuple=(255, 0, 0), thickWidth: int=2):
    """Draw a box and a label on an image with a given location
    
    Parameters
    -----
        img (np.array) -- image upon which the labeled box should be drawn
        top (int) -- top pixel of the box
        right (int) -- right pixel of the box
        bottom (int) -- bottom pixel of the box
        left (int) -- left pixel of the box
        label (str) -- text of the label
        font (int) -- font used for the label (default: cv2.FONT_HERSHEY_DUPLEX)
        textColor (tuple) -- color used for the label (default: (255, 255, 255))
        thickColor (tuple) -- color of the box (default: (255, 0, 0))
        thickWidth (int) -- thickness of the box (default: 2)
    
    Returns
    -----
        np.array -- a copy of the given image with the labeled box drawn on it
    """
    img_cpy = img.copy()
    cv2.rectangle(img_cpy, (left-20, top-20), (right+20, bottom+20), thickColor, thickWidth)        # draw a box around the face
    cv2.rectangle(img_cpy, (left-20, bottom-15), (right+20, bottom+20), thickColor, cv2.FILLED)     # draw a label bellow the box
    cv2.putText(img_cpy, label, (left -15, bottom + 15), font, 1.0, textColor, 1)                   # put the label text

    return img_cpy



def classifyFace(im: str, scaling: int=1) -> list:
    """Find all the faces in a given image and label them if they are known
    
    Parameters
    -----
        im (str) -- image file path
        scaling (int) -- scale value used to resize image before face recognition (default: 1)
    
    Returns
    -----
        list -- data about all encoded faces in the given img
    """
    knownFacesData  = getEncodedFaces(('jpg', 'jpeg', 'png'))
    facesEncoded    = [face['encoding'] for face in knownFacesData]
    knownFacesNames = [face['name'] for face in knownFacesData]

    # READ OUR IMAGE
    img = cv2.imread(im, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)                    # convert to BGR to fit face_recognition color model
    small_img = cv2.resize(img, (0, 0), fx=scaling, fy=scaling)   # resize to make face recognition faster    

    # FACE LOCATION AND ENCODING
    faceLocations = fr.face_locations(small_img)
    newFaces      = fr.face_encodings(small_img, faceLocations)

    data = []
    for face in newFaces:
        # SEE IF THE FACE IS MATCHING WITH A KNOWN ONE
        matches = fr.compare_faces(facesEncoded, face)
        name    = 'Unkown'
        # FIND THE KNOWN FACE WITH THE SMALLEST DISTANCE
        faceDistances  = fr.face_distance(facesEncoded, face)
        bestMatchIndex = np.argmin(faceDistances)
        if matches[bestMatchIndex]:
            name = knownFacesNames[bestMatchIndex]  # get the name of the face

        ##TODO : see if its posible to check if the image already exists, and don't append data if so
        data.append( {'imgPath': im, 'name': name, 'encoding': list(face), 'encoded_at': datetime.now()} )

        # DRAW A BOW AND A LABEL FOR THE FACE
        for location, d in zip(faceLocations, data):
            loc = tuple(int(l/scaling) for l in location)   # turn back face location to its original size
            img = drawLabeledBox(img, *loc, d['name'])      # add a labeled bow on the base untouched img

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # convert back to BGR since we display with opencv

    # DISPLAY RESULTING IMG
    while True:
        cv2.imshow('Video', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return data



# MAIN
if __name__ == "__main__":

    BASE_DIR = os.path.dirname(os.path.relpath(__file__))
    img = os.path.join(BASE_DIR, 'test.jpg')
    print(classifyFace(img, 0.6))