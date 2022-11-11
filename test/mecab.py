import os
import MeCab

import speech_recognition as sr
from pykakasi import kakasi

cmd_file = "0.bat"   # .cmdファイルへのパス
command = cmd_file

listener = sr.Recognizer()

try:
    with sr.Microphone() as source:
        print("Listening...")
#        voice = listener.listen(source)
#        voice_text = listener.recognize_google(voice, language="ja-JP")
#        print(voice_text)

        mecab= MeCab.Tagger()
        voice_text=('私は渡辺といいます。')  
        node = mecab.parseToNode(voice_text)  
        
        kakasi = kakasi()

        while node:
            
            print(node.surface)
            
            result = kakasi.convert(node.surface)
            print(result)
            
            text = result[0]['hira']
            print(text)
            if text == 'わたなべ':
                print('collect')
                os.system(command)
                break
 
            else:node = node.next
 
except:
    print('sorry I could not listen')
    