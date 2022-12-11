import numpy as np
import math as mh

def look_or_not(width, yaw, pitch):
    if yaw_judge(yaw) == 1 & pitch_judge(width, pitch) == 1:
        return 1
    else:
        return 0

def yaw_judge(yaw):
    threshold = 5
    if np.abs(yaw) <= threshold:
        return 1
    else:
        return 0

def pitch_judge(width, pitch):
    avg_width = 200.0 #1m離れた人の顔の幅平均
    #上の三角形の情報
    tall = 20 #カメラと人の頭の距離
    distance = width / avg_width * 100 #人とカメラの距離
    hypotenuse = (tall**2 + distance**2)**(1/2)#斜辺(三平方の定理より)

    #cosの計算(余弦定理)
    cos_value = (distance**2 + hypotenuse**2 - tall**2) / (2 * distance * hypotenuse)
    degree_value = mh.degrees(mh.acos(cos_value))

    #pitchの判定
    real_pitch = pitch - degree_value
    if real_pitch < 0:
        return 0 #上を向いているため
    else:
        glidient = mh.tan(mh.radians(real_pitch)) #傾きを求める
        look_position = glidient * distance #見ている位置を特定
        if look_position <= 150 | look_position >= 135:
            return 1 #おそらく頭を見ている
        else:
            return 0 #見てないからを返す

if __name__=="__main__":
    print(look_or_not(1,1,1))
