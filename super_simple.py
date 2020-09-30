import matplotlib.pyplot as plt
import pandas as pd
from pull_data import n_days_ago, n_hours_ago, pull

# 1. First we fetch the data from the source
# If you've already run this and have the file bitmex.pkl
# then you can comment these lines below and just load straight from disk.

# Pull the data from the exchange
df = pull(start=n_days_ago(5), symbol="XBTUSD")
# Save it to a file
df.to_pickle("bitmex.pkl")

# 2. We load the data

# Load it from the file
df = pd.read_pickle("bitmex.pkl")

# 3. Do some processing...

# 4. Graph the data

plt.style.use('dark_background')
plt.title("BTC spot price")
plt.plot(df.close)
plt.show()

