#実験結果をcsvファイルに書き込むもの
import faceAPIpart as face
import csv
import cv2
import keyboard
import numpy as np


if __name__=="__main__":
    cap = cv2.VideoCapture(0) #カメラを示す変数
    flag = 0 #最初の処理か否か判定する
    data = [0, 0, 0, 0, 0, 0, 0]
    label = ['roll', 'yaw', 'pitch', 'top', 'left', 'width', 'height']
    face_api = face.faceAPIpart()
    while True:
        if keyboard.is_pressed("e"): #eが押されたらカメラ写真をとる
            r, image = cap.read()
            temp_row = face_api.get_headPose(image)
            if len(temp_row) == 7: #異常値が帰ってきた場合は何もしない
                if flag == 0:
                    data = temp_row
                    flag = 1
                else:
                    data = np.vstack((data, temp_row))
        elif keyboard.is_pressed("q"): #qが押されたらwhile文を抜ける
            break
    # csvファイルにデータを記述する
    with open('data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(label)
        writer.writerows(data)
