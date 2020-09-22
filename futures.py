import matplotlib.pyplot as plt
import pandas as pd
import time
from pull_data import n_days_ago, n_hours_ago, pull

plt.style.use('dark_background')

days_ago = 10

symbol_perp = "XBTUSD"
df = pull(start=n_days_ago(days_ago), symbol=symbol_perp, bin_size="1m")
df.to_pickle("bitmex.pkl")
df = pd.read_pickle("bitmex.pkl")

#time.sleep(1)

symbol_futures = "XBTZ20"
df2 = pull(start=n_days_ago(days_ago), symbol=symbol_futures, bin_size="1m")
df2.to_pickle("bitmex-%s.pkl" % symbol_futures)
df2 = pd.read_pickle("bitmex-%s.pkl" % symbol_futures)

df = pd.concat([df.close, df2.close], keys=["XBTUSD", "XBTZ20"], axis=1)
df["spread"] = (df.XBTZ20 - df.XBTUSD) / df.XBTUSD
print(df)
print(df.spread.min())
print(df.spread.max())
print(df.spread.mean())

fig, (ax1, ax2) = plt.subplots(2, sharex=True,
    gridspec_kw={'hspace': 0, "height_ratios": [3, 1]})

ax1.set_title("Spread between %s and %s futures" % (symbol_perp, symbol_futures))

ax1.plot(df.XBTUSD)
ax1.plot(df.XBTZ20)

ax2.plot(df.spread)

plt.show()

