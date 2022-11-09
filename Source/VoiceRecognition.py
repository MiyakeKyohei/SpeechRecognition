# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import speech_recognition as sr
from pykakasi import kakasi

def main():
    listener = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            voice = listener.listen(source)
            voice_text = listener.recognize_google(voice, language="ja-JP")
            return voice_text
            
        """
            py_kakasi = kakasi()
            
            result = py_kakasi.convert(voice_text)
            print(result)
            
            text = result[0]['hira']
            
            if text == "わたなべ":
                print('collect')
        """
    except:
        return "読み取れませんでした"
        

if __name__=="__main__":
    n = 0
    while n < 10:
        voice_text = main()
        print(voice_text)
        n = n + 1