# -*- coding: utf-8 -*-

#import requests
import os
#import json
#import time
import numpy as np
import cv2
from datetime import datetime
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
#import matplotlib.pyplot as plt
import pandas as pd

##初期設定
cap = cv2.VideoCapture(0) #ひとまず0で内蔵カメラ。1にすると外付けカメラを使用できる
#csv_name = datetime.now().strftime('%Y%m%d_%H%M') #csvファイルとして保存するためのファイル名
data_name = ["roll", "yaw", "pitch"] #保存データの系列
headPose_data = [0, 0, 0]#初期値
count = 0 #撮影回数を示すカウンタ

#顔認識に用いる識別機の設定
cascade_path = 'C:\\Users\\kizuk\\anaconda3\\lib\\site-packages\\cv2\\data\\haarcascade_frontalface_alt.xml'
cascade = cv2.CascadeClassifier(cascade_path)

#サブスクリプションキーの設定
subscription_key = '43339af7313b481db1b97970b9599809'
assert subscription_key
#エンドポイントURLの設定
face_api_url = 'https://kmiyake-test.cognitiveservices.azure.com/'
#インスタンスの生成
face_client = FaceClient(face_api_url, CognitiveServicesCredentials(subscription_key))

#実行
while True:
    r, img = cap.read()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #グレースケールに変換
    #顔判定
    #minSizeで顔判定する時の最小の四角の大きさを指定出来る
    #minSizeが小さすぎると顔のシミまで顔と判断しかねないため
    faces = cascade.detectMultiScale(img_gray, scaleFactor = 1.1, minNeighbors = 1, minSize = (100, 100))
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if len(faces) > 0: #顔を検出した場合
        for face in faces:
            now = datetime.now()#撮影時間の取得
            os.makedirs("temp", exist_ok = True)
            filename = "temp\\number" + str(count) + '.jpg' #保存するファイル名
            cv2.imwrite(filename, img)#画像の書き出し
            
            #image_data = open(filename, 'rb').read()#処理する画像を選択する
            image_data = open(filename, 'rb')
            """
            headers = {'Ocp-Apim-Subscription-Key': subscription_key,
                       'Content-Type': 'application/octet-stream'}
            params = {
                'returnFaceId': 'true',
                'returnFaceLandMarks': 'false',
                'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
                }
            """
            params =["age", "gender", "headPose", "smile", "facialHair", "glasses", "emotion", "hair", "makeup", "occlusion", "accessories", "blur", "exposure", "noise"]
            #faceAPIで解析
            #response = requests.post(face_api_url, headers = headers, params = params, data = image_data)
            """
            params_temp = ["headPose"] #テスト用返却パラメータ
            response = face_client.face.detect_with_stream(image_data, return_face_attributes = params_temp)
            """
            response = face_client.face.detect_with_stream(image_data, return_face_attributes = params)
            
            #分析結果の表示q
            print(response[0].as_dict())

            response.raise_for_status()
            analysis = response.json() #json出力
            
            #faceのjsonから抽出したい項目をピックアップ
            result = [analysis[0]['faceAttributes']['headPose']['roll'],
                        analysis[0]['faceAttributes']['headPose']['yaw'],
                        analysis[0]['faceAttributes']['headPose']['pitch']]
            
            headPose_data = np.array(result) + np.array(headPose_data)
            
            df = pd.DataFrame({now:headPose_data},
                              index = data_name) #取得データをDataFrame1に変換してdfとして定義
            
            if count == 0: #初期
                df_past = df
                print(df)
            else:
                df = pd.concat([df_past, df], axis = 1, sort = False) #dfを更新
                print(df)
                
            '''
            plt.plot(df.T)#dfの行列を反転
            plt.legend(data_name)#凡例を表示
            plt.draw()#グラフ描画
            plt.pause(4)#ウェイト時間（=Azure更新時間）
            plt.cla()#グラフを閉じる
            '''

            count = count + 1#撮影回数の更新
            df_past = df #df_pastを更新
                
            
