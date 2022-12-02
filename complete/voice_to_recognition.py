import speech_recognition as sr

def convert_text():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        voice = listener.listen(source)
        voice_text = listener.recognize_google(voice, language="ja-JP")
        return voice_text