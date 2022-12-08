import speech_recognition as sr

def convert_text():
    listener = sr.Recognizer()
    #しきい値設定
    #listener.energy_threshold = 700 
    #listener.dynamic_energy_threshold=True
    #listener.dynamic_energy_adjustment_damping = 0.15 # type: float
    #listener.dynamic_energy_adjustment_ratio = 1.5 # type: float
    #listener.pause_threshold = 0.8 # type: float
    #listener.adjust_for_ambient_noise(source: AudioSource, duration: float = 1) -> None
    with sr.Microphone() as source:
        print("Listening...")
        #listener.adjust_for_ambient_noise(source, duration=1) 
        voice = listener.listen(source)
        voice_text = listener.recognize_google(voice, language="ja-JP")
        return voice_text