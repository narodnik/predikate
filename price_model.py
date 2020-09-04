import pandas as pd
import math
import numpy as np
import scipy.stats as st
from pull_data import n_days_ago, n_hours_ago, pull

#days_ago = 60
#df_btc = pull(start=n_days_ago(days_ago), symbol="XBTUSD")
#df_btc.to_pickle("bitmex-minutes-60d.pkl")
df_btc = pd.read_pickle("bitmex-minutes-60d.pkl")

#df_eth = pull(start=n_days_ago(days_ago), symbol="ETHUSD")
#df_eth.to_pickle("bitmex-eth-minutes-60d.pkl")
df_eth = pd.read_pickle("bitmex-eth-minutes-60d.pkl")

def analyze(df):
    df['logret'] = np.log(df.close) - np.log(df.close.shift(1))

    risk = 0.95
    time_period = 10 * 24 * 30
    var = df.logret.var() * time_period
    z_score = st.norm.ppf(risk)

    last_close = df.close.iloc[-1]
    print("Last close: %.0f" % last_close)

    stop_price = last_close * math.e**(-z_score * math.sqrt(var))
    print("Stop price: %.0f" % stop_price)

    n = 10000
    position_margin = n * (1/last_close - 1/stop_price)
    assert position_margin < 0
    initial_margin = n / last_close
    leverage = -initial_margin / position_margin
    print("Leverage: %.2fx" % leverage)

    mean = df.logret.mean()
    gain = math.e**(mean * time_period)
    roi = leverage * n * gain
    print("Return: %.0f$" % roi)

print()
print("Bitcoin:")
analyze(df_btc)

print()
print("Ethereum:")
analyze(df_eth)

