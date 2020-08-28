import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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
plt.xlim(-0.005, 0.005)
plt.show()

