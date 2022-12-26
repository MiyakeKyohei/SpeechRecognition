#実験結果をcsvファイルに書き込むもの
import faceAPIpart as face
import calculate as cl
import csv
import cv2
import keyboard
import numpy as np


if __name__=="__main__":
    cap = cv2.VideoCapture(0) #カメラを示す変数
    flag = 0 #最初の処理か否か判定する
    data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    label = ['roll', 'yaw', 'pitch', 'top', 'left', 'width', 'height', 'look_result', 'pitch_result', 'position']
    face_api = face.faceAPIpart()
    while True:
        if keyboard.is_pressed("e"): #eが押されたらカメラ写真をとる
            r, image = cap.read()
            temp_row = face_api.get_headPose(image)
            if len(temp_row) == 7: #異常値が帰ってきた場合は何もしない
                look_result = cl.look_or_not(temp_row[5], temp_row[1], temp_row[2])
                position_result = cl.pitch_judge(temp_row[5], temp_row[2])
                data_temp = np.hstack((temp_row, look_result, position_result))
                if flag == 0:
                    data = data_temp
                    flag = 1
                else:
                    data = np.vstack((data, data_temp))
        elif keyboard.is_pressed("q"): #qが押されたらwhile文を抜ける
            break
    # csvファイルにデータを記述する
    
    with open('data_test_07.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(label)
        writer.writerows(data)
