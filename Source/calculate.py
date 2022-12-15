import numpy as np
import math as mh

#外から呼び出す関数、見てたら1,見てないなら0
def look_or_not(width, yaw, pitch):
    if yaw_judge(yaw) == 1 & pitch_judge(width, pitch) == 1:
        return 1
    else:
        return 0

#Yawで見てるか判断する
def yaw_judge(yaw):
    threshold = 5 #閾値(未定)
    if np.abs(yaw) <= threshold:
        return 1
    else:
        return 0

def pitch_judge(width, pitch):
    avg_width = 200.0 #100cm離れた人の顔の幅平均(未定)
    #上の三角形の情報
    tall = 20 #カメラと人の頭の距離
    distance = avg_width / width * 100 #見てる人とカメラの距離(cm)
    hypotenuse = (distance**2 - tall**2)**(1/2)#底辺(三平方の定理より)

    #cosの計算(余弦定理)
    cos_value = (distance**2 + hypotenuse**2 - tall**2) / (2 * distance * hypotenuse)
    degree_value = mh.degrees(mh.acos(cos_value)) #角度(°を出す)

    #pitchの判定
    real_pitch = np.abs(pitch) - degree_value
    if real_pitch < 0:
        return 0 #上を向いているため
    else:
        glidient = mh.tan(mh.radians(real_pitch)) #傾きを求める
        look_position = (int)(glidient * hypotenuse) #見ている位置を特定
        if look_position <= 150 & look_position >= 135: #条件(未定)
            return 1 #おそらく頭を見ている
        else:
            return 0 #見てないからを返す

if __name__=="__main__":
    print(look_or_not(1,1,1))
