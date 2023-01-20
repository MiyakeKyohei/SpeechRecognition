#完成品
import databaseload
import voice_to_recognition
import pykakasi
import MeCab
import convert_hiragana_kakasi
import textmatching
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import faceAPIpart as f
import numpy as np
import calculate as cl
import keyboard
import videoCap as vcap
import threading
import time
#import mecab_split

look_result = 0
call_flag = 0

def system():
    #グローバル変数の指定
    global look_result
    global call_flag
    #テキストファイルopen
    datalist = databaseload.fopen()
    #以下の処理を繰り返す
    while True:
        if keyboard.is_pressed("q"): #qが押されたら抜ける(予定)
            break
        try:
            voice_text = voice_to_recognition.convert_text()#音声認識のファイル呼び込み
            if look_result == 1: #見ているか否か
                #以下、見ている場合の処理
                mecab = MeCab.Tagger()
                #node = mecab_split.msplit(voice_text)
                node = mecab.parseToNode(voice_text)#MeCab無理
                kakasi = pykakasi.kakasi()#インスタンス用
                while node:
                    text = convert_hiragana_kakasi.convert_hiragana(node,kakasi)#ひらがな変換
                    flag = textmatching.match(text,datalist)#テキストマッチングの結果
                    if flag == 1:
                        call_flag = 1
                        break
                    else:node = node.next#次の単語
            else:
                print("見ていません")
        except:
            print('sorry I could not listen')

def takeVideo():
    global look_result
    global call_flag
    cap = cv2.VideoCapture(0)
    face_api = f.faceAPIpart()
    fps = 0.70
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video = cv2.VideoWriter("video.mp4", fourcc, fps, (w, h))
    #filename="temp\\test.jpg"
    while True:
        t1 = time.time()
        r, image = cap.read()
        result_row = face_api.get_headPose(image)
        look_result = cl.look_or_not(result_row)
        vcap.drawImg(image, result_row, call_flag)
        cv2.imshow("img", image)
        video.write(image)
        cv2.imwrite("temp\\test.jpg", image)
        if keyboard.is_pressed("q"):
            break
        t2 = time.time()
        print("time is ", t2 -t1)
    cv2.destroyAllWindows()
    cap.release()
    video.release()


if __name__=="__main__":
    thread_1 = threading.Thread(target=system)
    thread_2 = threading.Thread(target=takeVideo)
    thread_1.start()
    thread_2.start()