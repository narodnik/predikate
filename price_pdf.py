import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
#from pull_data import n_days_ago, n_hours_ago, pull

df = pd.read_pickle("bitmex-minutes-60d.pkl")

df["P"] = np.log(df.close / 1000)
mean = df.P.mean()
var = df.P.var()

def lognstat(mu, sigma):
    """Calculate the mean of and variance of the lognormal distribution given
    the mean (`mu`) and standard deviation (`sigma`), of the associated normal 
    distribution."""
    m = np.exp(mu + sigma**2 / 2.0)
    v = np.exp(2 * mu + sigma**2) * (np.exp(sigma**2) - 1)
    return m, v

mean, var = lognstat(mean, np.sqrt(var))
stddev = np.sqrt(var)

last_close = df.close.iloc[-1] / 1000
#drift_price = mean * 10 + last_close

print(mean, last_close, stddev)
dist = stats.lognorm(s=stddev, scale=last_close)
#dist = stats.lognorm(s=1, scale=stddev, loc=last_close)

x = np.linspace(0, 20, 200)
plt.plot(x, dist.pdf(x))

plt.show()

