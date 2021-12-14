import matplotlib.pyplot as plt
import pandas as pd
import time
from pycoingecko import CoinGeckoAPI

def pull(coin_id, n_days_ago):
    cg = CoinGeckoAPI()

    time_now = int(time.time())
    time_delta = n_days_ago * 24 * 60 * 60

    chart = cg.get_coin_market_chart_range_by_id(
        coin_id, vs_currency="usd",
        from_timestamp=time_now - time_delta,
        to_timestamp=time_now)

    df = pd.DataFrame(chart["prices"],
                      columns=["time", "price"])
    df['time'] = pd.to_datetime(df['time'],unit='ms')
    df.set_index("time", inplace=True)

    return df

if __name__ == "__main__":
    df = pull("bitcoin", 30)
    print(df)
    plt.style.use('dark_background')
    plt.title("Portfolions")
    plt.plot(df.index, df.price)
    plt.show()

