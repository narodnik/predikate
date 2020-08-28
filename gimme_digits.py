import time
import math
import pandas as pd
import numpy as np
from pycoingecko import CoinGeckoAPI

def fetch_df():
    cg = CoinGeckoAPI()

    top_n = 200
    #n_days_ago = 50

    time_now = int(time.time())
    time_delta = 91 * 24 * 60 * 60

    df_r = pd.DataFrame()

    for i, coin in enumerate(cg.get_coins_markets(vs_currency="usd")[:top_n]):
        coin_id = coin["id"]
        chart = cg.get_coin_market_chart_range_by_id(
            coin_id, vs_currency="usd",
            from_timestamp=time_now - time_delta,
            to_timestamp=time_now)

        df = pd.DataFrame(chart["prices"],
                          columns=["time", "price"])
        df['time'] = pd.to_datetime(df['time'],unit='ms')
        df["time_delta"] = df.time - df.iloc[0].time
        df.set_index("time_delta", inplace=True)

        df["%s" % coin_id] = np.log(df.price) - np.log(df.iloc[0].price)
        df.drop(columns=["time", "price"], inplace=True)
        df = df.iloc[1:]
        df = df.transpose()
        df_r = df_r.append(df)

        print(i, coin_id)
        time.sleep(.15)

    print(df_r)
    print()
    print(df_r.idxmax(axis = 0))
    return df_r

#df = fetch_df()
#df.to_pickle("winners.pkl")
df = pd.read_pickle("winners.pkl")

df_r = pd.DataFrame()

for column_name, series in df.iteritems():
    series = series.sort_values(ascending=False)
    series = series.reset_index()
    series.columns = ["coins", "returns"]
    series = series.coins
    series = series.apply(lambda coin: coin.replace("-return", ""))
    df_r[column_name] = series

df = df_r
df.to_csv("top_picks.csv")
#print(df)
