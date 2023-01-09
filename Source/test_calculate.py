import faceAPIpart as face
import calculate as cl
import cv2
import keyboard
import numpy as np

if __name__=="__main__":
    cap = cv2.VideoCapture(0)
    face_api = face.faceAPIpart()

    while True:
        if keyboard.is_pressed("e"):
            r, image = cap.read()
            result_row = face_api.get_headPose(image)
            print("HeadPose is : ", result_row)
            look_result = cl.look_or_not(result_row)
            print("look result is : ", look_result)
        elif keyboard.is_pressed("q"):
            break