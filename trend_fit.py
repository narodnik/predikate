import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
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

coin_id = sys.argv[1] if len(sys.argv) > 1 else "bitcoin"

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
R = np.exp(slope * 60 * 24)
print("R: %0.2f" % R)

#days = (r.index - r.index[0]) / pd.Timedelta(minutes=1)
#slope, intercept, correlation, p_val_1, stderr_1 = \
#    stats.linregress(days, r)
#
#print("Correlation:", correlation)

plt.style.use('dark_background')
plt.title("Trend for %s\n Correlation = %.2f   Daily Return = %.0f %%" % (
    coin_id, correlation, 100 * R))
plt.plot(df.index, slope * (df.index - df.index[0]) / pd.Timedelta(minutes=1) + intercept)
plt.plot(df.index, df.p)
#plt.scatter(df.index, df.r, 0.1)

#figure = plt.gcf()
#figure.set_size_inches(10, 7)
#plt.savefig("images/trend-%s.png" % coin_id, dpi=100)

fig_manager = plt.get_current_fig_manager()
fig_manager.window.showMaximized()
plt.show()

