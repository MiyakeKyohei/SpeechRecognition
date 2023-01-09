import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import norm
import pandas as pd
sns.set()

#データの読み込み
df = pd.read_csv("data\\muramatsu_data.csv")
df_yaw = df["yaw"].to_numpy()

#正規分布描画用データ作成
x = np.linspace(-7.5, 7.5, 1000)
y = norm.pdf(x, loc=0.2076086956521739, scale=4.051260152890587**0.5)

fig, ax = plt.subplots()
ax.hist(df_yaw, density=True, label='data')
ax.plot(x, y, label="pdf")
ax.legend()
ax.set_xlim(-7.5, 7.5)
ax.set_ylim(0, 0.4)
ax.set_xlabel("yaw")
ax.set_ylabel("density")
plt.savefig("yaw_graph.png")
