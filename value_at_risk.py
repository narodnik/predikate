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

monthly_btc_mean_gain = math.e**(df.btc_logret.mean() * minutes_in_a_month)
monthly_eth_mean_gain = math.e**(df.eth_logret.mean() * minutes_in_a_month)

print("BTC monthly average gain in 1 month: %.0f %%" %
    (monthly_btc_mean_gain * 100))
print("ETH monthly average gain in 1 month: %.0f %%" %
    (monthly_eth_mean_gain * 100))

monthly_btc_var = df.btc_logret.var() * minutes_in_a_month
monthly_eth_var = df.eth_logret.var() * minutes_in_a_month

print("BTC variance:", monthly_btc_var)
print("ETH variance:", monthly_eth_var)

monthly_btc_stddev = math.sqrt(monthly_btc_var)
monthly_eth_stddev = math.sqrt(monthly_eth_var)

monthly_btc_stddev = math.e**-monthly_btc_stddev
monthly_eth_stddev = math.e**-monthly_eth_stddev

print("BTC standard deviation (1 month):", monthly_btc_stddev)
print("ETH standard deviation (1 month):", monthly_eth_stddev)

gain_ratio = monthly_eth_mean_gain / monthly_btc_mean_gain
print("Ethereum is %.0f %% more profitable than Bitcoin" % (gain_ratio * 100))
risk_ratio = monthly_eth_stddev / monthly_btc_stddev
print("But the ratio of risk is %.0f %%" % (risk_ratio * 100))

print("Covariance (1 month):")
print(df.cov() * minutes_in_a_month)

z_score = st.norm.ppf(.95)
print("z score:", z_score)

btc_interval = z_score * math.sqrt(df.btc_logret.var() * minutes_in_a_month)
print("+/- z sigma:", btc_interval)

current_price = 11850
lower_bound = current_price * math.e**-btc_interval
print("lower bound:", lower_bound)

btc_mean = df.btc_logret.mean() * minutes_in_a_month
conf_low = current_price * math.e**(btc_mean - btc_interval) 
conf_high = current_price * math.e**(btc_mean + btc_interval) 

print("confidence: [%.0f, %.0f]" % (conf_low, conf_high))

monthly_logreturn = df.btc_logret.mean() * minutes_in_a_month
next_avg_price = current_price * math.e**monthly_logreturn
print("price target:", next_avg_price)

