import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
import random
from pull_data import n_days_ago, pull

current_price = 10100

df = pull(start=n_days_ago(45), bin_size="1d")
df.to_pickle("bitmex-daily-60d.pkl")

df = pd.read_pickle("bitmex-daily-60d.pkl")
percent_changes = df["vwap"].pct_change()
log_return = np.log(df.vwap) - np.log(df.vwap.shift(1))
print(log_return)

mean, stddev = log_return.mean(), log_return.std()
print("Mean=%s Stddev=%s" % (mean, stddev))

liquidation_price = 7000

def run_single_simulation(start_price, stop_price):
    price = start_price
    for i in range(30):
        price_log_return = random.normalvariate(mean, stddev)
        price = price * math.exp(price_log_return)
        if price < stop_price:
            return price
    return price

def run_simulations(start_price, stop_price):
    total = 20000
    prices = []
    for i in range(total):
        price = run_single_simulation(start_price, stop_price)
        prices.append(price)
    return prices

def simulate_pnls():
    xvalues = []
    yvalues = []

    for stop_price in range(2000, current_price, 500):
        print("Running simulation for stop_price:", stop_price)
        end_prices = run_simulations(current_price, stop_price)

        pnls = []
        for exit_price in end_prices:
            pnl = (1 - current_price / exit_price)
            pnls.append(pnl)

        average_pnl = sum(pnls) / len(pnls)
        print("Average PNL:", average_pnl)

        xvalues.append(stop_price)
        yvalues.append(average_pnl)
    return xvalues, yvalues

def pnl_histogram_data(stop_price):
    end_prices = run_simulations(current_price, stop_price)
    pnls = []
    for exit_price in end_prices:
        pnl = (1 - current_price / exit_price)
        pnls.append(pnl)
    return pnls

#xvalues, yvalues = simulate_pnls()

plt.style.use('dark_background')

#plt.title("Average PNL for different liquidation prices. Start price=%s" %
#    current_price)

plt.title("Distribution of PNL outcomes frequencies vs stop prices")

ax = plt.gca()
ax.yaxis.set_label_position("right")
ax.yaxis.tick_right()

for stop_price in [8000, 8500, 9000]:
    pnls = pnl_histogram_data(stop_price)
    ax.hist(pnls, bins=100, alpha=0.5, label="Stop: %s" % stop_price)

#ax.plot(xvalues, yvalues)

plt.legend()
plt.show()

