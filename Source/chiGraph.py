import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2
from matplotlib import animation as ani
from scipy import stats


k = 1
n = 30000
threshold = stats.chi2.ppf(0.99, 1)
print(threshold)
print(stats.chi2.interval(0.98, 1)[1])
cum = np.zeros(n)
for i in range(k):
    x = np.random.normal(0, 1, n)
    x2 = x**2
    cum += x2


plt.ylim(0, 0.5)
plt.xlim(0, 7)
#plt.grid()
plt.xlabel("Anomaly Score")
plt.ylabel("Density")
#plt.hist(cum, 80, color="lightgreen", normed=True)
xx = np.linspace(0, 25, 1000)
plt.plot(xx, chi2.pdf(xx, df=k, scale=1), linewidth=2, color='b')
plt.vlines(threshold, ymin=0, ymax=5, ls="solid", color='r')
plt.savefig("chi2Graph.png")
