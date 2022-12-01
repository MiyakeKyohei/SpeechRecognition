# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 22:27:40 2022

@author: kyohe
"""

import requests
import os
import json
import time
import numpy as np
import cv2
from datetime import datetime
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
#import matplotlib.pyplot as plt
import pandas as pd
from azure.cognitiveservices.vision.face.models import FaceAttributeType

##初期設定
cap = cv2.VideoCapture(0) #ひとまず0で内蔵カメラ。1にすると外付けカメラを使用できる
#csv_name = datetime.now().strftime('%Y%m%d_%H%M') #csvファイルとして保存するためのファイル名
data_name = ["roll", "yaw", "pitch"] #保存データの系列
headPose_data = [0, 0, 0]#初期値
count = 0 #撮影回数を示すカウンタ

#顔認識に用いる識別機の設定
cascade_path = 'C:\\Users\\kyohe\\anaconda3\\lib\\site-packages\\cv2\\data\\haarcascade_frontalface_alt.xml'
cascade = cv2.CascadeClassifier(cascade_path)

#サブスクリプションキーの設定
KEY = '43339af7313b481db1b97970b9599809'
#エンドポイントURLの設定
ENDPOINT = 'https://kmiyake-test.cognitiveservices.azure.com/'

#実行
while True:
    r, img = cap.read()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #グレースケールに変換
    #顔判定
    #minSizeで顔判定する時の最小の四角の大きさを指定出来る
    #minSizeが小さすぎると顔のシミまで顔と判断しかねないため
    faces = cascade.detectMultiScale(img_gray, scaleFactor = 1.1, minNeighbors = 1, minSize = (100, 100))
    
    if (cv2.waitKey(1) & 0xFF == ord('q')) | count > 1:
        break

    if len(faces) > 0: #顔を検出した場合
        for face in faces:
            now = datetime.now()#撮影時間の取得
            os.makedirs("temp", exist_ok = True)#写真保存用のディレクトリを作成(あれば何もしない)
            filename = "temp\\number" + str(count) + '.jpg' #保存するファイル名
            cv2.imwrite(filename, img)#画像の書き出し
            
            image_data = open(filename, "rb")#処理する画像を選択する
            #faceAPIで解析
            response = requests.post(ENDPOINT + "face/v1.0/detect?returnFaceAttributes=headPose", data=image_data, headers={"Ocp-Apim-Subscription-Key": KEY, "Content-Type": "application/octet-stream"})
            analysis = response.json() #json出力
            print(analysis)
            
            #faceのjsonから抽出したい項目を配列に入れる
            result = [analysis[0]['faceAttributes']['headPose']['roll'],
                        analysis[0]['faceAttributes']['headPose']['yaw'],
                        analysis[0]['faceAttributes']['headPose']['pitch']]
            
            headPose_data = np.array(result)
            print(headPose_data)
            #df = pd.DataFrame({now:headPose_data}, index = data_name) #取得データをDataFrame1に変換してdfとして定義
            
            if count == 0: #初期
                df = np.array(result)
                df_past = df
            else:
                df = pd.concat([df, np.array(result)]) #dfを更新

            count = count + 1#撮影回数の更新
            df_past = df #df_pastを更新
                
            
