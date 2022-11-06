import time
import speech_recognition as sr
import pyaudio


SAMPLERATE = 44100

def callback(in_data, frame_count, time_info, status):
    global sprec
    try:
        audiodata = sr.AudioData(in_data, SAMPLERATE * 2)
        sprec_text = sprec.recognize_google(audiodata, language = 'ja-JP')
        print(sprec_text)
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        pass
    finally:
        return (None, pyaudio.paContinue)


def main():
    global sprec
    sprec = sr.Recognizer()
    #Audioインスタンスを取得
    audio = pyaudio.PyAudio()
    stream = audio.open(format = pyaudio.paInt16,
                            rate = SAMPLERATE,
                            channels = 1,
                            input_device_index = 1,
                            input = True,
                            frames_per_buffer = SAMPLERATE * 2, #2秒周期でコールバック
                            stream_callback = callback)
    stream.start_stream()
    while stream.is_active():
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    audio.terminate()

if __name__=='__main__':
    main()

