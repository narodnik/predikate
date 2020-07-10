import matplotlib.pyplot as plt
import pandas as pd
from pull_data import n_days_ago, pull

df = pull(start=n_days_ago(10))
df.to_pickle("bitmex.pkl")

df = pd.read_pickle("bitmex.pkl")

lookback = 14 * 60
d_fast_period = 3 * 60
d_slow_period = 3 * 60

#lookback = 48 * 60
#d_fast_period = 3 * 60
#d_slow_period = 6 * 60

lows = df["low"].rolling(lookback).min()
highs = df["high"].rolling(lookback).max()
k = (df["close"] - lows) / (highs - lows)
d_fast = k.rolling(d_fast_period).mean()
d_slow = d_fast.rolling(d_slow_period).mean()
print(lows)
print(highs)


plt.style.use('dark_background')

fig, (ax1, ax2) = plt.subplots(2, sharex=True,
    gridspec_kw={'hspace': 0, "height_ratios": [3, 1]})

ax1.set_title("BTC-USD Adj Close Price")
ax1.plot(df.index, df["vwap"], lw=1, alpha=0.8,
         label="Bitcoin Price (BitMex)")

ax1.grid(which='major', color='#666666', linestyle=':')
ax1.minorticks_on()
ax1.grid(which='minor', color='#999999', linestyle='-', alpha=0.2)

ax1.yaxis.set_label_position("right")
ax1.yaxis.tick_right()

ax2.set_title("Stochastic indicator")
ax2.plot(k, lw=1, alpha=0.8, label="K stochastic")
ax2.plot(d_fast, lw=3, alpha=0.8, label="D fast stochastic")
ax2.plot(d_slow, lw=3, alpha=0.8, label="D slow stochastic")
ax2.axhline(y=0.2, color='r', linestyle='-')
ax2.axhline(y=0.8, color='r', linestyle='-')
ax2.set_ylim(ymin=0, ymax=1)

#plt.tick_params(labelsize=12)
fig.legend(loc='upper left', fontsize=12)
fig.autofmt_xdate()
plt.savefig("images/stochastic.png")
plt.show()

