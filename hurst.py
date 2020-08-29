import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from pull_data import n_days_ago, n_hours_ago, pull

symbol = "XBTUSD"
ticks = "1m"
days_ago = 30

filename = "bitmex-%s-%s-%s" % (symbol, ticks, days_ago)
#df = pull(start=n_days_ago(days_ago), symbol=symbol, bin_size=ticks)
#df.to_pickle(filename)
df = pd.read_pickle(filename)

min_lag = 0
max_lag = 500
from_date = df.index[-1] - pd.DateOffset(days=10)

lags = range(0, max_lag)
changes = [np.log(df.close) - np.log(df.close.shift(lag)) for lag in lags]
variances = [change.loc[from_date:].var() for change in changes]

df = pd.DataFrame(variances, columns=["vars"])
df.index += 1
df.index = np.log(df.index)
df.vars = np.log(df.vars)

df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)

lr = LinearRegression()
lr.fit(df.index.values.reshape(-1, 1), df.vars.values.reshape(-1, 1))
m = lr.coef_[0][0]
c = lr.intercept_[0]
plt.plot(df.index, df.index * m + c)

print("Slop/intercept:", m, c)
hurst = m / 2
print("Hurst exponent:", m / 2)

plt.scatter(df.index, df.vars, 0.1)
plt.show()

#variances = [(np.log(df.close) 
#print(lags)
#np.log(df.close) - np.log(df.close.shift(lag)

