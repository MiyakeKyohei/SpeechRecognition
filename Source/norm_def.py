#yawの出方が正規分布に従っているか判定するためのプログラム
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
import numpy as np

#データの読み込み
df_sample = pd.read_csv("data_test_06.csv")

#シャピロウィルクの検定
result1 = stats.shapiro(df_sample["pitch"])
print(result1)

#コルゴモロフ・スミルノフ検定
result2 = stats.ks_1samp(df_sample["pitch"], stats.norm.cdf)
print(result2)

yaw_sample = df_sample["pitch"].to_numpy()
#カーネル関数はガウシアンモデルでフィット
kde = KernelDensity(kernel='gaussian', bandwidth=0.1).fit(yaw_sample[:,None])
#入力用データ
x = np.linspace(-20, 20, 2000)[:,None]

#KernelDesityモデルで確率密度計算
dens = kde.score_samples(x)

#描画用figを準備
plt.plot(x, np.exp(dens), color='orange')
plt.savefig("test_pitch.png")