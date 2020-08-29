import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from pull_data import n_days_ago, n_hours_ago, pull

symbol = "XBTUSD"
ticks = "1m"
days_ago = 30

filename = "bitmex-%s-%s-%s" % (symbol, ticks, days_ago)
#df = pull(start=n_days_ago(days_ago), symbol=symbol, bin_size=ticks)
#df.to_pickle(filename)
df = pd.read_pickle(filename)

min_lag = 1
max_lag = 30
date_offset = pd.DateOffset(hours=5)

def calculate_hurst(df, min_lag, max_lag, date_offset, plot=True):
    from_date = df.index[-1] - date_offset

    lags = range(min_lag, max_lag)
    changes = [np.log(df.close) - np.log(df.close.shift(lag)) for lag in lags]
    variances = [change.loc[from_date:].var() for change in changes]

    df = pd.DataFrame(variances, index=lags, columns=["vars"])
    df.index = np.log(df.index)
    df.vars = np.log(df.vars)

    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)

    slope, intercept, correlation, p_val_1, stderr_1 = \
        stats.linregress(df.index, df.vars)
    #print("Slope/intercept:", slope, intercept)
    hurst = slope / 2
    print("Hurst exponent:", hurst)
    print("Correlation:", correlation)
    print()

    if plot:
        plt.style.use('dark_background')
        plt.title("Hurst exponent")
        plt.plot(df.index, slope * df.index + intercept)
        plt.scatter(df.index, df.vars, 0.1)
        plt.show()

    return hurst, correlation

def make_hursts():
    idx = []
    hursts = []
    corrs = []
    increments = int(30 * 24 / 5)
    for i in range(0, increments):
        until_date = df.index[-1] - pd.DateOffset(hours=i * 5)
        dfx = df.loc[:until_date]
        hurst, corr = calculate_hurst(dfx, min_lag, max_lag,
                                      date_offset, plot=False)
        price = dfx.iloc[-1].close
        index = dfx.index[-1]

        corrs.append(corr)
        hursts.append(hurst)
        idx.append(index)

    values = list(zip(hursts, corrs))
    dfh = pd.DataFrame(values, index=idx, columns=["hurst", "corr"])
    return dfh

filename = "hurst.pkl"
dfh = make_hursts()
dfh.to_pickle(filename)
dfh = pd.read_pickle(filename)

print(dfh)

plt.style.use('dark_background')

fig, (ax1, ax2) = plt.subplots(2, sharex=True,
    gridspec_kw={'hspace': 0, "height_ratios": [3, 1]})

ax1.set_title("Price and hurst exponent")
ax1.yaxis.set_label_position("right")
ax1.yaxis.tick_right()

ax1.grid(which='major', color='#666666', linestyle=':')
ax1.minorticks_on()
ax1.grid(which='minor', color='#999999', linestyle='-', alpha=0.2)

ax1.plot(df.index, df.close, lw=1, alpha=0.8,
    label="Close price")

#ax2.plot(
#    dfh.loc[dfh["corr"] > 0.9].index, 
#    dfh.hurst[dfh["corr"] > 0.9],
#    'x', markersize=10, color='#009900', label="Strong signal (>0.9 corr)")
#
#dfh["const"] = 0.5
#ax2.plot(
#    dfh.loc[dfh["corr"] <= 0.9].index, 
#    dfh.const[dfh["corr"] <= 0.9],
#    'o', markersize=10, color='#990000', label="Bad signal")

ax2.plot(dfh.index, dfh.hurst, label="Hurst exponent")
ax2.axhline(y=0.5, color='r', linestyle='-')
ax2.set_ylim(ymin=0, ymax=1)

fig.legend(loc='upper left', fontsize=12)
plt.show()

