import faceAPIpart as face
import calculate as cl
import cv2
import keyboard
import numpy as np

def drawImg(image, result_row):
    try:
        for i in range(len(result_row)):
            if i != 0:
                roll = result_row[i, 0]
                yaw = result_row[i, 1]
                pitch = result_row[i, 2]
                top = int(result_row[i, 3])
                left = int(result_row[i, 4])
                width = int(result_row[i, 5])
                height = int(result_row[i, 6])
                #四角入力
                cv2.rectangle(image, #図形入力画像
                            (left, top), #始点
                            (left + width, top + height), #終点
                            (255 * (i % 2), 255 * int(i % 2), 0), #色
                            5) #線の大きさ
                #テキストの描画
                Text = ["roll : " + str(roll), "yaw : " + str(yaw), "pitch : " + str(pitch)]
                for j in range(3):
                    cv2.putText(image,
                                Text[j],
                                (left, top - 10 - 20 * (2- j)),
                                fontFace=cv2.FONT_HERSHEY_COMPLEX,
                                fontScale=0.5,
                                color=(255 * (i % 2), 255 * int(i % 2), 0),
                                thickness=1)
    except:
        print("error")

if __name__=="__main__":
    flag = 0
    cap = cv2.VideoCapture(0)
    face_api = face.faceAPIpart()
    fps = 1
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video = cv2.VideoWriter("video.mp4", fourcc, fps, (w, h))
    while True:
        if flag < 20:
            r, image = cap.read()
            result_row = face_api.get_headPose(image)
            drawImg(image, result_row)
            cv2.imshow("img", image)
            video.write(image)
            cv2.waitKey(1000)
            cv2.imwrite("temp\\test.jpg", image)
            flag = flag + 1
            if keyboard.is_pressed("q"):
                break
    cv2.destroyAllWindows()
    cap.release()
    video.release()