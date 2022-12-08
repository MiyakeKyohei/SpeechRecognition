import requests
import json
import numpy as np
import cv2
import os

class faceAPIpart:
    #顔認識に用いる識別機の設定
    #直接ディレクトリに置いても動きそう
    #cascade_path = 'C:\\Users\\kyohe\\anaconda3\\lib\\site-packages\\cv2\\data\\haarcascade_frontalface_alt.xml'
    cascade_path = 'haarcascade_frontalface_alt.xml'
    cascade = cv2.CascadeClassifier(cascade_path)

    #サブスクリプションキーの設定
    KEY = '43339af7313b481db1b97970b9599809'
    #エンドポイントURLの設定
    ENDPOINT = 'https://kmiyake-test.cognitiveservices.azure.com/'
    ##初期設定
    #cap = cv2.VideoCapture(0)#ひとまず0で内蔵カメラ。1にすると外付けカメラを使用できる
    unable_Pose = [180, 180, 180] #あり得ない値

    #faceAPIpartのクラスのインスタンスを定義するメソッド
    def __init__(self):
        headPose_data = [0, 0, 0]

    #カスケード分類器を用いて顔があるか判定する関数
    def cascade_judge(image): #imageはビデオから得た画像データ
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #グレースケールに変換
        #顔判定
        #minSizeで顔判定する時の最小の四角の大きさを指定出来る
        #minSizeが小さすぎると顔のシミまで顔と判断しかねないため
        faces = faceAPIpart.cascade.detectMultiScale(img_gray, scaleFactor = 1.1, minNeighbors = 1, minSize = (100, 100))
        if len(faces) > 0:
            return 1
        else:
            return 0

    #faceAPIからの戻り値を行列に直し、返すメソッド
    def get_faceAPI_result(filename):
        image_data = open(filename, "rb")#処理する画像を選択する
        #faceAPIで解析
        response = requests.post(faceAPIpart.ENDPOINT + "face/v1.0/detect?returnFaceAttributes=headPose", data=image_data, headers={"Ocp-Apim-Subscription-Key": faceAPIpart.KEY, "Content-Type": "application/octet-stream"})
        analysis = response.json() #json出力
        #行列の生成
        analysis_len = len(analysis) #検出した顔の個数
        index = 0 #配列のインデックス
        result = faceAPIpart.unable_Pose #返却用配列の初期化
        #faceのjsonから抽出したい項目を配列に入れる
        while index < analysis_len:
            result_temp = [analysis[index]['faceAttributes']['headPose']['roll'],
                        analysis[index]['faceAttributes']['headPose']['yaw'],
                        analysis[index]['faceAttributes']['headPose']['pitch']]
            #行列の生成
            if index == 0:
                result = result_temp
            else:
                result = np.vstack((result, result_temp))
            index = index + 1
        #結果の出力
        return np.array(result)

    #imageデータをtempに保存する関数
    def saveImage(filename, image):
        os.makedirs("temp", exist_ok = True)#写真保存用のディレクトリを作成(あれば何もしない)
        cv2.imwrite(filename, image)#画像の書き出し

    #imageデータから顔の向きを返す関数
    def get_headPose(image):
        try:
            if faceAPIpart.cascade_judge(image) == 1:
                filename = "temp\\target.jpg"
                faceAPIpart.saveImage(filename, image)
                return faceAPIpart.get_faceAPI_result(filename)
            else:
                return faceAPIpart.unable_Pose
        except:
            return faceAPIpart.unable_Pose

if __name__=="__main__":
    cap = cv2.VideoCapture(0)
    count = 0
    while count < 1:
        r, image = cap.read()
        print(faceAPIpart.get_headPose(image))
        count = count + 1