#pitchとwidthの関係を探るプログラム
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
import numpy as np
from statistics import mean, variance
from scipy.spatial import distance

#データの読み込み
df = pd.read_csv("data_test_06.csv")
df = df[["pitch", "width"]]

df_sample = df.to_numpy()

#平均値
means = np.mean(df_sample, axis=0)
print(means)

#分散共分散行列
cov_mat = np.cov(df_sample.T)
cov_i_mat = np.linalg.pinv(cov_mat)
print(cov_i_mat)

result = distance.mahalanobis([50, -20], means, cov_i_mat)
print("マハラノビス距離 : ", result)
#threshold = stats.chi2.interval(0.90, 1)[1]
#print("threshold : ", threshold)
print("x : ", stats.chi2.ppf(q = 0.99, df = 1))

#散布図の描画
plt.scatter(df_sample[:, 0], df_sample[:, 1])
plt.xlabel("pitch")
plt.ylabel("width")
plt.grid(True)
plt.savefig("pitch_width_06.png")