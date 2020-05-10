import matplotlib.pyplot as plt
import pandas as pd
import random
from pull_data import n_days_ago, pull

#df = pull(start=n_days_ago(100), bin_size="1d")
#df.to_pickle("bitmex-daily-100d.pkl")

df = pd.read_pickle("bitmex-daily-100d.pkl")
percent_changes = df["vwap"].pct_change()
mean, stddev = percent_changes.mean(), percent_changes.std()
#print(mean, stddev)

plt.style.use('dark_background')

current_price = 10000
liquidation_price = 7000

total = 1000
count = 0
for i in range(total):
    prices = []
    price = current_price
    for i in range(30):
        price += price * random.normalvariate(mean, stddev)
        if price < liquidation_price:
            count += 1
            break
        prices.append(price)
    plt.plot(prices)

plt.title("Percentage of liquidations: %.2f%% (bankruptcy=%s, start price=%s)" % (
    (count / total) * 100,
    liquidation_price,
    current_price))

ax = plt.gca()
ax.yaxis.set_label_position("right")
ax.yaxis.tick_right()

plt.savefig("images/montecarlo.png")
plt.show()

