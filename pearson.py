import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pull_data import n_days_ago, pull
import  yfinance as yf
from datetime import timedelta, datetime

#number of days
n = 10
# get stock data from yahoo finance
stock = yf.Ticker("GOOG")
dfyh = stock.history(period=f"{n*2}d", interval="1d")
dfyh = dfyh.filter(['Close'], axis=1)
dfyh = dfyh.rename(columns={"Close" : "yh_close"})


# set timezone to None in dfyh
dfyh.index = dfyh.index.tz_localize(tz=None)
start_date = dfyh.index[0:1].to_pydatetime()[0].astimezone(tz=None)

# get bitcoin/usd data from bitmex
dfbtc = pull(start=start_date, bin_size="1d")
dfbtc.to_pickle("bitmex.pkl")
dfbtc = pd.read_pickle("bitmex.pkl")

# set timezone to None in dfbtc
dfbtc.index = dfbtc.index.tz_localize(tz=None)

dfbtc = dfbtc.filter(['close'], axis=1)
dfbtc = dfbtc.rename(columns={"close" : "btc_close"})

df = dfbtc.join(dfyh)
df = df[df['yh_close'] > 0]


# test
corr = df['btc_close'].corr(df['yh_close'])
print(corr)

plt.style.use('dark_background')

fig, (ax1, ax2) = plt.subplots(2, sharex=True,
        gridspec_kw={'hspace': 0, "height_ratios": [2,2]})

# ax1
ax1.set_title("BTC-USD Adj Close Price")
ax1.plot(df.index, df["btc_close"], lw=2, alpha=0.8,
        label="Bitcoin Price (BitMex)")
ax1.plot(df.index, df["yh_close"], lw=1, alpha=0.3,
        label="Stock Price (Yahoo Finance) ")
ax1.grid(which='major', color='#666666', linestyle=':')
ax1.minorticks_on()
ax1.grid(which='minor', color='#999999', linestyle='-', alpha=0.2)
ax1.yaxis.set_label_position("right")
ax1.yaxis.tick_right()

# ax2
ax2.set_title("Pearson")
ax2.set_ylim(ymin=-1, ymax=1)

fig.legend(loc='upper left', fontsize=12)
fig.autofmt_xdate()
plt.savefig("images/pearson.png")
#plt.show()

