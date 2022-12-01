#完成品
import databaseload
import voice_to_recognition
import pykakasi
import MeCab
import convert_hiragana_kakasi
import textmatching
import cv2
import faceAPIpart
#import mecab_split

#テキストファイルopen
datalist = databaseload.fopen()
cap = cv2.VideoCapture(0)

try:
    
    voice_text = voice_to_recognition.convert_text()#音声認識のファイル呼び込み
    print(voice_text)
    
    r, image = cap.read()
    print(faceAPIpart.get_headPose(image))
    
    #node = mecab_split.msplit(voice_text)
    
    mecab = MeCab.Tagger()
    node = mecab.parseToNode(voice_text)#MeCab無理
 
    kakasi = pykakasi.kakasi()#インスタンス用
    """
    if __name__=="__main__":
        count = 0
        while count < 1:
            r, image = cap.read()
            print(faceAPIpart.get_headPose(image))
            count = count + 1
    """
    
    while node:
        
        text = convert_hiragana_kakasi.convert_hiragana(node,kakasi)#ひらがな変換
        
        flag = textmatching.match(text,datalist)#テキストマッチングの結果

        if flag == 1:
            print('終了しました。')
            break
        else:node = node.next#次の単語
 
except:
    print('sorry I could not listen')
    

