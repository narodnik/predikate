import matplotlib.pyplot as plt
import pandas as pd
from pull_data import n_days_ago, n_hours_ago, pull

df = pull(start=n_days_ago(5), symbol="XBTUSD")
df.to_pickle("bitmex.pkl")
df = pd.read_pickle("bitmex.pkl")

plt.style.use('dark_background')
plt.title("BTC spot price")
plt.plot(df.close)
plt.show()

