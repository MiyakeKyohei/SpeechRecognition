import cv2
import threading
import keyboard
import voice_to_recognition

def takeVideo():
    filename="test.mp4"
    print("Start")
    cap = cv2.VideoCapture(0)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video = cv2.VideoWriter(filename, fourcc, 1, (w, h))
    while True:
        r, image = cap.read()
        cv2.imshow("img", image)
        video.write(image)
        cv2.imwrite("temp\\test.jpg", image)
        if keyboard.is_pressed("q"):
                break
    cv2.destroyAllWindows()
    video.release()
    cap.release()

def voiceRecognition():
    while True:
        text = voice_to_recognition.convert_text()
        print(text)

if __name__=="__main__":
    thread_1 = threading.Thread(target=takeVideo)
    #thread_2 = threading.Thread(target=takeVideo,args=(cap, "test2.mp4"))
    thread_2 = threading.Thread(target=voiceRecognition)
    thread_1.start()
    thread_2.start()
