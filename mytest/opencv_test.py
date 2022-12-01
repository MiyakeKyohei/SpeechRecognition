# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 12:42:53 2022

@author: kyohe
"""

import cv2
from datetime import datetime


cap = cv2.VideoCapture(0)
#顔認識に用いる識別機の設定
cascade_path = 'C:\\Users\\erenn\\anaconda3\\lib\\site-packages\\cv2\\data\\haarcascade_frontalface_alt.xml'
cascade = cv2.CascadeClassifier(cascade_path)
count = 0
while True:
    ret, img = cap.read()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(img_gray, scaleFactor = 1.1, minNeighbors = 1, minSize = (100, 100))

    if len(faces) > 0: #顔を検出した場合
        for face in faces:
            now = datetime.now()#撮影時間の取得
            filename = "temp\\number" + str(count) + ".jpg" #保存するファイル名
            print(filename)
            cv2.imwrite(filename, img)#画像の書き出し

    count = count + 1
    if count >= 3:
        break


    
cap.release()
cv2.destroyAllWindows()