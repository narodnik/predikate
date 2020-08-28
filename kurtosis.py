import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import pandas as pd
from pull_data import n_days_ago, n_hours_ago, pull

symbol = "XBTUSD"
ticks = "1m"
days_ago = 30

filename = "bitmex-%s-%s-%s" % (symbol, ticks, days_ago)
#df = pull(start=n_days_ago(days_ago), symbol=symbol, bin_size=ticks)
#df.to_pickle(filename)
df = pd.read_pickle(filename)

df["r"] = np.log(df.close) - np.log(df.close.shift(1))

mu = df.r.mean()
var = df.r.var()
sigma = np.sqrt(var)

print("Mean:", mu)
print("Var:", var)
print("Skew:", df.r.skew())
print("Kurtosis:", df.r.kurtosis())
print("N:", len(df))

sns.distplot(df.r)

x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
plt.plot(x, stats.norm.pdf(x, mu, sigma))

plt.xlim(-0.005, 0.005)
plt.show()

