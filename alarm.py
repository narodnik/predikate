import time
import toml
import os
from bitmex import bitmex

upper_limit = 10000
lower_limit = 9000

with open("config.toml", "r") as file:
    config = toml.loads(file.read())

bitmex_api_key = config["bitmex_api_key"]
bitmex_api_secret = config["bitmex_api_secret"]
music_path = config["alarm_music"]

bitmex_client = bitmex(
    test=False,
    api_key=bitmex_api_key,
    api_secret=bitmex_api_secret)

def get_last_price():
    last_trade = bitmex_client.Trade.Trade_get(
        symbol="XBTUSD", count=1, reverse=True).result()[0][0]
    return last_trade["price"]

def display_price(price):
    print()
    print("********************************")
    print(price)
    print("********************************")
    print()

def play_music():
    os.system("bash -c \"mplayer -loop 0 %s &> /dev/null\"" % music_path)

while True:
    last_price = get_last_price()
    if last_price >= upper_limit or last_price <= lower_limit:
        display_price(last_price)
        play_music()
    time.sleep(2)

