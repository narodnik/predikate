import matplotlib.pyplot as plt
import numpy as np
from pull_data import n_days_ago, n_hours_ago, pull

window_long = {
    "days_ago": 100,
    "ticks": "1d",
    "alpha": 0.9
}

window_short = {
    "days_ago": 5,
    "ticks": "1m",
    "alpha": 0.01
}

#active_window = window_long
active_window = window_short

symbols = [
    "XBTUSD",
    "ETHUSD"
]

def single_plot(axes, symbol):
    days_ago = active_window["days_ago"]
    ticks = active_window["ticks"]
    alpha = active_window["alpha"]

    df = pull(start=n_days_ago(days_ago), symbol=symbol, bin_size=ticks)

    df['log_ret'] = np.log(df.close) - np.log(df.close.shift(1))

    df["ema_log_ret"] = df.log_ret.ewm(alpha=alpha).mean()
    df["ema_log_var"] = df.log_ret.ewm(alpha=alpha).var()

    ax1, ax2 = axes

    #ax1.plot(df.index, df.log_ret, lw=1, alpha=0.8)
    ax1.plot(df.index, df.ema_log_ret, lw=1, alpha=0.8,
        label="logreturn %s" % symbol)

    ax2.plot(df.index, df.ema_log_var, label="%s variance" % symbol)

plt.style.use('dark_background')

fig, (ax1, ax2) = plt.subplots(2, sharex=True,
    gridspec_kw={'hspace': 0, "height_ratios": [3, 1]})

ax1.set_title("Logreturn and Variance since %s days ago" %
    active_window["days_ago"])
ax1.yaxis.set_label_position("right")
ax1.yaxis.tick_right()

ax1.grid(which='major', color='#666666', linestyle=':')
ax1.minorticks_on()
ax1.grid(which='minor', color='#999999', linestyle='-', alpha=0.2)

for symbol in symbols:
    single_plot((ax1, ax2), symbol)

fig.legend(loc='upper left', fontsize=12)
plt.show()
