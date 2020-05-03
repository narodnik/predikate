import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pull_data import n_days_ago, pull

df = pull(start=n_days_ago(10))
df.to_pickle("bitmex.pkl")

df = pd.read_pickle("bitmex.pkl")
# bin size = 1 minute
# window = time / bin_size
#window = 5 * 60
#df["sma-5hr"] = df["vwap"].rolling(window=window).mean()
#window = 1 * 24 * 60
#df["sma-1day"] = df["vwap"].rolling(window=window).mean()
#window = 5 * 24 * 60
#df["sma-5day"] = df["vwap"].rolling(window=window).mean()

short_window = 5 * 60
df["ema-5hr"] = df["vwap"].ewm(span=short_window).mean()
long_window = 1 * 24 * 60
df["ema-1day"] = df["vwap"].ewm(span=long_window).mean()

df["signal"] = 0.0
df["signal"] = np.where(df["ema-5hr"] > df["ema-1day"], 1.0, 0.0)
df["position"] = df["signal"].diff()

df["macd"] = df["ema-5hr"] - df["ema-1day"]

df.rename(columns = {'vwap':'price'}, inplace=True)
df = df[n_days_ago(5):]

#plt.grid(True)
#plt.plot(df["price"], label="price")
#df[["price", "ema-5hr", "ema-1day"]].plot()
#plt.show()

plt.style.use('dark_background')

fig, (ax1, ax2) = plt.subplots(2, sharex=True,
    gridspec_kw={'hspace': 0, "height_ratios": [3, 1]})

ax1.set_title("BTC-USD Adj Close Price")
ax1.plot(df.index, df["price"], lw=1, alpha=0.8,
         label="Bitcoin Price (BitMex)")
ax1.plot(df.index, df["ema-5hr"], lw=3, alpha=0.8,
         label="EMA (Exponential Moving Average) - 5 hours")
ax1.plot(df.index, df["ema-1day"], lw=3, alpha=0.8,
         label="EMA 1 day")

ax1.plot(df.loc[df["position"] == 1.0].index, 
         df["ema-5hr"][df["position"] == 1.0],
         '^', markersize=10, color='r', label="Buy signal")
         
ax1.plot(df.loc[df["position"] == -1.0].index, 
         df["ema-5hr"][df["position"] == -1.0],
         'v', markersize=10, color='#555555', label="Sell signal")

ax1.grid(which='major', color='#666666', linestyle=':')
ax1.minorticks_on()
ax1.grid(which='minor', color='#999999', linestyle='-', alpha=0.2)

ax1.yaxis.set_label_position("right")
ax1.yaxis.tick_right()

macd = df["macd"].iloc[::100]
ax2.set_title("MACD indicator")
ax2.bar(macd.index, macd, width=0.01)

#plt.tick_params(labelsize=12)
fig.legend(loc='upper left', fontsize=12)
plt.savefig("images/macd.png")
plt.show()

