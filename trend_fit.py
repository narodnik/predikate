import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
from pycoingecko import CoinGeckoAPI
from scipy import stats

days_ago = 30

coins = [
    "solana",
    "polkadot",
    "bzx"
]

cg = CoinGeckoAPI()

time_now = int(time.time())
#time_delta = 91 * 24 * 60 * 60
time_delta = 12 * 24 * 60 * 60

coin_id = "bitcoin"
chart = cg.get_coin_market_chart_range_by_id(
    coin_id, vs_currency="usd",
    from_timestamp=time_now - time_delta,
    to_timestamp=time_now)

df = pd.DataFrame(chart["prices"],
                  columns=["time", "price"])
df['time'] = pd.to_datetime(df['time'],unit='ms')
df.set_index("time", inplace=True)

df["p"] = np.log(df.price)
df["r"] = np.log(df.price) - np.log(df.price.shift(1))
df.dropna(inplace=True)

print(df)

z = np.abs(stats.zscore(df.r))
r = df.r[z < 3]
print(r)
#print(z)

#print(df)
days = (df.index - df.index[0]) / pd.Timedelta(minutes=1)
slope, intercept, correlation, p_val_1, stderr_1 = \
    stats.linregress(days, df.p)

print("Correlation: %0.2f" % correlation)

#days = (r.index - r.index[0]) / pd.Timedelta(minutes=1)
#slope, intercept, correlation, p_val_1, stderr_1 = \
#    stats.linregress(days, r)
#
#print("Correlation:", correlation)

plt.style.use('dark_background')
plt.title("Trend for %s. Correlation = %0.2f" % (coin_id, correlation))
plt.plot(df.index, slope * (df.index - df.index[0]) / pd.Timedelta(minutes=1) + intercept)
plt.plot(df.index, df.p)
#plt.scatter(df.index, df.r, 0.1)
plt.show()

