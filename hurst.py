import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from pull_data import n_days_ago, n_hours_ago, pull

symbol = "XBTUSD"
ticks = "1m"
days_ago = 30

filename = "bitmex-%s-%s-%s" % (symbol, ticks, days_ago)
#df = pull(start=n_days_ago(days_ago), symbol=symbol, bin_size=ticks)
#df.to_pickle(filename)
df = pd.read_pickle(filename)

min_lag = 1
max_lag = 8 * 60
date_offset = pd.DateOffset(days=10)

def calculate_hurst(df, min_lag, max_lag, date_offset, plot=True):
    from_date = df.index[-1] - pd.DateOffset(days=10)

    lags = range(min_lag, max_lag)
    changes = [np.log(df.close) - np.log(df.close.shift(lag)) for lag in lags]
    variances = [change.loc[from_date:].var() for change in changes]

    df = pd.DataFrame(variances, index=lags, columns=["vars"])
    df.index = np.log(df.index)
    df.vars = np.log(df.vars)

    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)

    lr = LinearRegression()
    lr.fit(df.index.values.reshape(-1, 1), df.vars.values.reshape(-1, 1))
    m = lr.coef_[0][0]
    c = lr.intercept_[0]

    print("Slope/intercept:", m, c)
    hurst = m / 2
    print("Hurst exponent:", m / 2)

    if plot:
        plt.style.use('dark_background')
        plt.title("Hurst exponent")
        plt.plot(df.index, df.index * m + c)
        plt.scatter(df.index, df.vars, 0.1)
        plt.show()

    return hurst

hurst = calculate_hurst(df, min_lag, max_lag, date_offset)

