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
#import mecab_split


if __name__=="__main__":
    #テキストファイルopen
    datalist = databaseload.fopen()
    cap = cv2.VideoCapture(0)
    face_api = f.faceAPIpart()
    #以下の処理を繰り返す
    while True:
        if keyboard.is_pressed("q"): #qが押されたら抜ける(予定)
            break
        try:
            voice_text = voice_to_recognition.convert_text()#音声認識のファイル呼び込み
            #print(voice_text)
            r, image = cap.read() #画像の読み込み
            result = face_api.get_headPose(image)
            #print(result)
            if cl.look_or_not(result) == 1: #見ているか否か
                #以下、見ている場合の処理
                mecab = MeCab.Tagger()
                #node = mecab_split.msplit(voice_text)
                node = mecab.parseToNode(voice_text)#MeCab無理

                kakasi = pykakasi.kakasi()#インスタンス用
                while node:
                    
                    text = convert_hiragana_kakasi.convert_hiragana(node,kakasi)#ひらがな変換
                    
                    flag = textmatching.match(text,datalist)#テキストマッチングの結果

                    if flag == 1:
                        #print('終了しました。')
                        break
                    else:node = node.next#次の単語
            else:
                print("見ていません")
        except:
            print('sorry I could not listen')
