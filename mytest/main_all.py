#完成品

import os
import MeCab

import speech_recognition as sr
from pykakasi import kakasi

cmd_file = "0.bat"   # .cmdファイルへのパス
command = cmd_file

listener = sr.Recognizer()
#テキストファイルopen
f = open('database.txt', 'r', encoding='UTF-8')

datalist = f.readlines()

f.close()

try:
    with sr.Microphone() as source:
        print("Listening...")
        voice = listener.listen(source)
        voice_text = listener.recognize_google(voice, language="ja-JP")
        print(voice_text)

        mecab = MeCab.Tagger()
        node = mecab.parseToNode(voice_text)  
        
        kakasi = kakasi()
        flag = 0#一致時(i=1)while文から抜けるためのflag
        
        #print(node.surface)
        
        while node:
            
            print(node.surface)#テキスト化されたワード
            
            result = kakasi.convert(node.surface)#変換
            text = result[0]['hira']#平仮名を取り出す
            print(text)
            for w in datalist:
                if text == w.split('\n',1)[0]:#wに\nが含まれているから
                    print('collect')
                    os.system(command)#音量0
                    flag = 1
                    break

            if flag == 1:
                break
            else:node = node.next#次の単語
            
 
except:
    print('sorry I could not listen')
