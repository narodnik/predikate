import pandas as pd
import math
import numpy as np
import scipy.stats as st
from pull_data import n_days_ago, n_hours_ago, pull

days_ago = 30

#df_btc = pull(start=n_days_ago(days_ago), symbol="XBTUSD")
#df_btc.to_pickle("bitmex-minutes-60d.pkl")
df_btc = pd.read_pickle("bitmex-minutes-60d.pkl")

#df_eth = pull(start=n_days_ago(days_ago), symbol="ETHUSD")
#df_eth.to_pickle("bitmex-eth-minutes-60d.pkl")
df_eth = pd.read_pickle("bitmex-eth-minutes-60d.pkl")

df_btc['btc_logret'] = np.log(df_btc.close) - np.log(df_btc.close.shift(1))
df_eth['eth_logret'] = np.log(df_eth.close) - np.log(df_eth.close.shift(1))

df = pd.concat([df_btc.btc_logret, df_eth.eth_logret], axis=1)
df = df.dropna()

minutes_in_a_month = 60 * 24 * 30

print("BTC log mean (1 month):", df.btc_logret.mean() * minutes_in_a_month)
print("ETH log mean (1 month):", df.eth_logret.mean() * minutes_in_a_month)
print("BTC variance (1 month):", df.btc_logret.var() * minutes_in_a_month)
print("ETH variance (1 month):", df.eth_logret.var() * minutes_in_a_month)
print("Covariance (1 month):")
print(df.cov() * minutes_in_a_month)

z_score = st.norm.ppf(.95)
print("z score:", z_score)

btc_interval = z_score * math.sqrt(df.btc_logret.var() * minutes_in_a_month)
print("+/- z sigma:", btc_interval)

current_price = 11850
lower_bound = current_price * math.e**-btc_interval
print("lower bound:", lower_bound)

monthly_logreturn = df.btc_logret.mean() * minutes_in_a_month
next_avg_price = current_price * math.e**monthly_logreturn
print("price target:", next_avg_price)

