#import tsagdata
#results = tsagdata.TSAG_GetData(bins='1h', start="2020-04-01 12:00")
#df = results.run()

import pandas as pd
import math
import pytz
import time
import toml
from datetime import timedelta, datetime
from bitmex import bitmex

#symbol = "XBTUSD"
#bin_size = "1m"

with open("config.toml", "r") as file:
    config = toml.loads(file.read())

bitmex_api_key = config["bitmex_api_key"]
bitmex_api_secret = config["bitmex_api_secret"]

bitmex_client = bitmex(
    test=False,
    api_key=bitmex_api_key,
    api_secret=bitmex_api_secret)

#first = bitmex_client.Trade.Trade_getBucketed(
#    symbol=symbol,
#    binSize=bin_size,
#    count=1,
#    reverse=False).result()[0]
#first = first[0]

def n_days_ago(n):
    return datetime.now(pytz.utc) - timedelta(days=n)

def n_hours_ago(n):
    return datetime.now(pytz.utc) - timedelta(hours=n)

def date_from_string(datestring):
    date = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    date = pytz.utc.localize(start)
    return date

def pull(start=None, end=None, bin_size="1m", symbol="XBTUSD"):
    last = bitmex_client.Trade.Trade_getBucketed(
        symbol=symbol,
        binSize="1m",
        count=1,
        reverse=True).result()[0]
    last = last[0]

    if start is None:
        start = n_days_ago(5)

    if end is None:
        end = last["timestamp"]

    print("Downloading from Bitmex")
    print()

    print("Start =", start)
    print("End   =", end)
    print()

    binsizes = {"1m": 1, "5m": 5, "1h": 60, "1d": 1440}
    batch_size = 750

    delta_minutes = (last["timestamp"] - start).total_seconds() / 60
    available_data = math.ceil(delta_minutes / binsizes[bin_size])
    rounds = math.ceil(available_data / batch_size)

    print('Downloading %d minutes of new data available for %s, i.e. %d instances of %s data in %d rounds.' % (
        delta_minutes, symbol, available_data, bin_size, rounds))

    data_df = pd.DataFrame()

    round_increment = batch_size * binsizes[bin_size]
    for current_round in range(rounds):
        time.sleep(0.1)

        new_time = (start + timedelta(minutes = current_round * round_increment))
        
        data = bitmex_client.Trade.Trade_getBucketed(
            symbol=symbol,
            binSize=bin_size,
            count=batch_size,
            startTime = new_time).result()[0]

        temp_df = pd.DataFrame(data)
        data_df = data_df.append(temp_df)

    data_df.set_index('timestamp', inplace=True)
    return data_df

def clean(self, df):
    df.rename(columns = {'timestamp':'time'}, inplace=True)

if __name__ == "__main__":
    df = pull()

