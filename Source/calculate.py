import numpy as np
import math as mh

def get_real_height(height, pitch):
    return height / mh.cos((pitch / 180) + mh.pi)

def get_ytics(height, pitch):
    real_height = get_real_height(height, pitch)
    return avg_height / real_height

def look_or_not(top, left, height, width, yaw, pitch):
    face_x = left + (width / 2) #x座標
    face_y = top + (height / 2) #y座標
    glidient = mh.tan(((90 - yaw) / 180) * mh.pi) #傾き
    hashi_x = face_x + (480 - face_y) / glidient
    return hashi_x

print("hashi_x = :", look_or_not(228, 300, 148, 148, 38.8, 9.3))
