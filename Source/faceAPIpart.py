import requests
import json
import numpy as np
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import calculate as cl
#import os

class faceAPIpart:
    #顔認識に用いる識別機の設定
    #直接ディレクトリに置いても動きそう
    #cascade_path = 'C:\\Users\\kyohe\\anaconda3\\lib\\site-packages\\cv2\\data\\haarcascade_frontalface_alt.xml'
    cascade_path = 'haarcascade_frontalface_alt.xml'
    cascade = cv2.CascadeClassifier(cascade_path)

    #サブスクリプションキーの設定
    #KEY = '43339af7313b481db1b97970b9599809'(以前のやつ)
    KEY = '12300f103f6041ea8cf703d62c22a5c8'
    #エンドポイントURLの設定
    #ENDPOINT = 'https://kmiyake-test.cognitiveservices.azure.com/'(旧エンドポイント)
    ENDPOINT = 'https://miyakenewface.cognitiveservices.azure.com/'
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
    def get_faceAPI_result(self, filename):
        try:
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
                            analysis[index]['faceAttributes']['headPose']['pitch'],
                            analysis[index]['faceRectangle']['top'],
                            analysis[index]['faceRectangle']['left'],
                            analysis[index]['faceRectangle']['width'],
                            analysis[index]['faceRectangle']['height']]
                #行列の生成
                if index == 0:
                    result = np.vstack((result_temp, result_temp))
                else:
                    result = np.vstack((result, result_temp))
                index = index + 1
            #結果の出力
            return np.array(result)
        except:
            return faceAPIpart.unable_Pose

    #imageデータをtempに保存する関数
    def saveImage(filename, image):
        os.makedirs("temp", exist_ok = True)#写真保存用のディレクトリを作成(あれば何もしない)
        cv2.imwrite(filename, image)#画像の書き出し

    #imageデータから顔の向きを返す関数
    def get_headPose(self, image):
        try:
            #if faceAPIpart.cascade_judge(image) == 1:
            filename = "temp\\target.jpg" #撮影した画像をtemp\\target.jpgに保存
            faceAPIpart.saveImage(filename, image)
            return faceAPIpart.get_faceAPI_result(filename)
        except:
            return faceAPIpart.unable_Pose


if __name__=="__main__":
    cap = cv2.VideoCapture(0)
    count = 0
    while count < 1:
        r, image = cap.read()
        ret_array = faceAPIpart.get_headPose(image)
        if cl.look_or_not(ret_array[5], ret_array[1], ret_array[2]) == 1:
            print("見ている")
        else:
            print("見ていない")
        count = count + 1
