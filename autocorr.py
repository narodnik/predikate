import numpy as np
import pandas as pd
from pull_data import n_days_ago, n_hours_ago, pull

symbol = "XBTUSD"
ticks = "1m"
days_ago = 30

filename = "bitmex-%s-%s-%s.pkl" % (symbol, ticks, days_ago)
#df = pull(start=n_days_ago(days_ago), symbol=symbol, bin_size=ticks)
#df.to_pickle(filename)
df = pd.read_pickle(filename)
df = df.iloc[-200:]

df["r"] = np.log(df.close) - np.log(df.close.shift(1))

# rho = sum[(r_t - u)(r_{t-1} - u)] / sum[(r_t - u)^2]

lag = 1
diff = df.r - df.r.mean()
corr = (diff * diff.shift(lag)).sum() / (diff**2).sum()
print(corr)

