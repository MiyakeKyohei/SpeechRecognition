import os

import speech_recognition as sr
from pykakasi import kakasi

cmd_file = "0.bat"   # .cmdファイルへのパス
command = cmd_file

listener = sr.Recognizer()

try:
    with sr.Microphone() as source:
        print("Listening...")
        voice = listener.listen(source)
        voice_text = listener.recognize_google(voice, language="ja-JP")
        print(voice_text)
        
        kakasi = kakasi()
        
        result = kakasi.convert(voice_text)
        print(result)
        
        text = result[0]['hira']

        if text == 'わたなべ':
            print('collect')
            os.system(command)
except:
    print('sorry I could not listen')
    