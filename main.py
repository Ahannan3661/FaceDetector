import os
import pickle
import time

import cv2
import face_recognition
import numpy as np

def recognizeFace(image):
    imgS = cv2.resize(image, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace, tolerance=0.5)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            print(faceDis)
            print(matches)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                return True
        return False


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

background = cv2.imread('resources/background.png')

recognized = cv2.imread('resources/Modes/3.png')
active = cv2.imread('resources/Modes/1.png')

print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds

print("Encode File Loaded")

found = False
t0 = 100
background[44:44 + 633, 808:808 + 414] = active

while True:

    success, img = cap.read()

    if found:
        if time.clock() - t0 > 5:
            found = False
            t0 = time.clock()
            background[44:44 + 633, 808:808 + 414] = active
    else:
        if recognizeFace(img):
            t0 = time.clock()
            found = True
            background[44:44 + 633, 808:808 + 414] = recognized

    background[162:162+480, 55:55+640] = img

    cv2.imshow("Face Recognizer", background)

    cv2.waitKey(1)
