import numpy as np
import math as mh
from scipy import stats
from scipy.spatial import distance
import cv2
import faceAPIpart as face
#外から呼び出す関数,見てたら1,見てないなら0
def look_or_not(result):# 返却された行列をそのままま引数とする.
    try:
        for i in range(len(result)): #送られてきた人数分のデータをさらう
            yaw = result[i, 1]
            width = result[i, 5]
            pitch = result[i, 2]
            #if yaw_judge(yaw) == 1 and pitch_judge(width, pitch) == 1:
            if yaw_judge(yaw) == 1 and new_pitch_judge(pitch) == 1:
                return 1 #誰かが向いていたら1を返す
        return 0 #誰も向いていないので0を返す
    except:
        return 0 #何らかのエラーもしくは顔が映っていない

#Yawで見てるか判断する
def yaw_judge(yaw):
    #村松君のデータを基にしています
    # 有意水準0.01でシャピロウィルク検定を使用すると正規分布に従うと考えられたため
    threshold = stats.chi2.ppf(0.99, 1) #閾値(有意水準0.01)
    yaw_mean = 0.2076086956521739 #データの平均値
    yaw_variance = 4.051260152890587 #データの分散
    anomaly_score = (yaw - yaw_mean)**2 / yaw_variance #データの異常度
    if anomaly_score <= threshold: #異常度が閾値以下
        return 1 #見ている
    else:
        return 0 #見ていない

def new_pitch_judge(pitch):
    #村松君のデータを基にしています
    # 有意水準0.01でシャピロウィルク検定を使用すると正規分布に従うと考えられたため
    threshold = stats.chi2.ppf(0.99, 1) #閾値(有意水準0.01)
    pitch_mean = 4.21 #データの平均値
    pitch_variance = 13.017482758620691 #データの分散
    anomaly_score = (pitch - pitch_mean)**2 / pitch_variance #データの異常度
    if anomaly_score <= threshold: #異常度が閾値以下
        return 1 #見ている
    else:
        return 0 #見ていない

def pitch_judge(width, pitch):
    #使用する値の定義
    data = np.array([pitch, width]) #判定するデータ
    means = np.array([-4.48695652,66.76086957]) #村松君のデータの平均
    cov_i = np.array([[0.0700944 ,0.0128131] 
                    ,[0.0128131, 0.00400041]]) #村松君のデータの分散共分散の逆行列
    threshold = stats.chi2.ppf(0.99, 2) #閾値(自由度2,有意水準0.01)
    #マハラノビス距離の算出
    mh_distance = distance.mahalanobis(data, means, cov_i)**2
    if mh_distance <= threshold:
        return 1
    else:
        return 0

"""
def pitch_judge(width, pitch):
    avg_width = 120.0 #100cm離れた人の顔の幅平均(おおよそ確定)
    look_position = -1 #返却用変数(後に何か入れるがエラー時はそのまま)
    #上の三角形の情報
    tall = 30 #カメラと人の頭の距離(カメラが高さ200cm設定)
    distance = avg_width / width * 100 #見てる人とカメラの距離(cm)
    if distance - tall < 0: #下の処理のエラー処理
        return np.array([-100, look_position])
    hypotenuse = (distance**2 - tall**2)**(1/2)#底辺(三平方の定理より)

    #cosの計算(余弦定理)
    cos_value = (distance**2 + hypotenuse**2 - tall**2) / (2 * distance * hypotenuse)
    degree_value = mh.degrees(mh.acos(cos_value)) #角度(°を出す)

    #pitchの判定
    real_pitch = np.abs(pitch) - degree_value
    if real_pitch < 0:
        return np.array([-1, look_position]) #上を向いているため
    else:
        glidient = mh.tan(mh.radians(real_pitch)) #傾きを求める
        look_position = (int)(glidient * hypotenuse) #見ている位置を特定
        print("look_position is :",look_position)
        if look_position <= 85 and look_position >= 40: #条件(未定)
            return np.array([1, look_position]) #おそらく頭を見ている
        else:
            return np.array([0, look_position]) #おそらく見ていない
if __name__=="__main__":
    cap = cv2.VideoCapture(0)
    r, image = cap.read()
    face_api = face.faceAPIpart()
    temp_row = face_api.get_headPose(image)
    look_result = look_or_not(temp_row)
    print(look_result)
"""
