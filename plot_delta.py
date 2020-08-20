import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
from pull_data import n_days_ago, n_hours_ago, pull

#df_btc = pull(start=n_days_ago(days_ago), symbol="XBTUSD")
#df_btc.to_pickle("bitmex-minutes-60d.pkl")
df_btc = pd.read_pickle("bitmex-minutes-60d.pkl")

#df_eth = pull(start=n_days_ago(days_ago), symbol="ETHUSD")
#df_eth.to_pickle("bitmex-eth-minutes-60d.pkl")
df_eth = pd.read_pickle("bitmex-eth-minutes-60d.pkl")

#df_eth["eth_returns"] = df_eth.close - df_eth.close.shift(1)
#df_btc["btc_returns"] = df_btc.close - df_btc.close.shift(1)

df_eth['eth_returns'] = np.log(df_eth.close) - np.log(df_eth.close.shift(1))
df_btc['btc_returns'] = np.log(df_btc.close) - np.log(df_btc.close.shift(1))

df = pd.concat([df_btc.btc_returns, df_eth.eth_returns], axis=1)
df = df.dropna()

plt.style.use('dark_background')

fig, ax = plt.subplots()

ax.set_title("ETH minute returns vs BTC minute returns")
ax.grid(which='major', color='#666666', linestyle=':')
ax.minorticks_on()
ax.grid(which='minor', color='#999999', linestyle='-', alpha=0.2)

ax.scatter(df.eth_returns, df.btc_returns, s=1)

plt.show()
