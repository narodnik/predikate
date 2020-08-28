import time
import math
import pandas as pd
import numpy as np
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

coins = [
    "bitcoin",
    "litecoin",
    "ethereum"
]

bases = ["usd", "eur"]

top_n = 8
n_days_ago = 50

time_now = int(time.time())
time_delta = 91 * 24 * 60 * 60

df_r = pd.DataFrame()

for i, coin in enumerate(cg.get_coins_markets(vs_currency="usd")[:top_n]):
    coin_id = coin["id"]
    chart = cg.get_coin_market_chart_range_by_id(
        coin_id, vs_currency="usd",
        from_timestamp=time_now - time_delta,
        to_timestamp=time_now)

    df = pd.DataFrame(chart["prices"][:n_days_ago + 1],
                      columns=["time", "price"])
    df['time'] = pd.to_datetime(df['time'],unit='ms')
    df["time_delta"] = df.time - df.iloc[0].time
    df.set_index("time_delta", inplace=True)

    df["%s-return" % coin_id] = np.log(df.price) - np.log(df.iloc[0].price)
    df.drop(columns=["time", "price"], inplace=True)
    df = df.iloc[1:]
    df = df.transpose()
    #print(df)
    df_r = df_r.append(df)
    #log_returns = []
    #last_price = None
    #last_timestamp = None
    #for timestamp, price in chart["prices"][:10]:
    #    if last_price is None:
    #        last_price = price
    #        last_timestamp = timestamp
    #        continue

    #    price_change = math.log(price / last_price)
    #    timestamp_change = timestamp - last_timestamp

    #    if timestamp_change != 24 * 60 * 60 * 1000:
    #        price_change = None

    #    last_price = price
    #    last_timestamp = timestamp

    #    log_returns.append(price_change)

    #ohlc = cg.get_coin_ohlc_by_id(
    #    coin_id, vs_currency="usd", days=10)
    print(i, coin_id)
    #print(log_returns)

print(df_r)
print()
print(df_r.idxmax(axis = 0))

#for coin in cg.get_coins_list()[:100]:
#    coin_id = coin["id"]
#    print(coin_id)
#    status = cg.get_coin_status_updates_by_id(coin_id)
#    print(status)
#    time.sleep(.125 * 2)

#print(cg.get_price(ids=coins, vs_currencies=bases))
#print(cg.get_price(
#    ids='bitcoin', vs_currencies='usd',
#    include_market_cap='true', include_24hr_vol='true',
#    include_24hr_change='true', include_last_updated_at='true'
#))
#print(cg.get_supported_vs_currencies())
#print(cg.get_coins_markets(vs_currency="usd"))
#print(cg.get_derivatives())

