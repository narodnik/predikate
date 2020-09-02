import matplotlib.pyplot as plt
import pandas as pd
import time
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

time_now = int(time.time())
time_delta = 12 * 24 * 60 * 60

coins = {
    #"uniswap": 50,
    #"bitcoin": 10,
    #"chainlink":        20,
    "polkadot":         20,
    "solana":           20,
    #"yfvalue":          5,
    #"swipe":            5,
    #"ocean-protocol":   5,
    "curio":            5,
    #"tellor":           5,
    #"kleros":           5,
    #"s/statera":        5,
    #"synthetix-network-token": 0,
    #"aave":             0,
    #"yearn-finance":    5,
    #"kava":             5,
}

total_shares = sum(coins.values())

df = pd.DataFrame()

for coin_id, position in coins.items():
    print("Fetch:", coin_id)
    chart = cg.get_coin_market_chart_range_by_id(
        coin_id, vs_currency="usd",
        from_timestamp=time_now - time_delta,
        to_timestamp=time_now)

    dfp = pd.DataFrame(chart["prices"],
                      columns=["time", coin_id])
    dfp['time'] = pd.to_datetime(dfp['time'],unit='ms')
    dfp.set_index("time", inplace=True)

    start_price = dfp[coin_id].iloc[0]
    last_price = dfp[coin_id].iloc[-1]
    delta_price = last_price - start_price

    dfp[coin_id] -= start_price
    dfp[coin_id] /= delta_price

    df = pd.concat([df, dfp], axis=1)

df["price"] = 0
for coin_id, position in coins.items():
    df[coin_id] = df[coin_id].interpolate()
    weight = position / total_shares
    df.price += weight * df[coin_id]

print(df)

plt.style.use('dark_background')
plt.title("Portfolions")
plt.plot(df.index, df.price, lw=4)

for coin_id, _ in coins.items():
    plt.plot(df.index, df[coin_id], alpha=0.4)

fig_manager = plt.get_current_fig_manager()
fig_manager.window.showMaximized()
plt.show()

