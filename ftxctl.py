import ccxt
import pprint
import toml

with open("config.toml", "r") as file:
    config = toml.loads(file.read())

ftx_api_key = config["ftx_api_key"]
ftx_api_secret = config["ftx_api_secret"]

exchange = ccxt.ftx({
    'apiKey': ftx_api_key,
    'secret': ftx_api_secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future',
    },
})

print("Positions:")
for position in exchange.fetch_positions():
    if position["size"] > 0:
        #pprint.pprint(position)
        print(position["future"])
        print("  PNL:\t", position["realizedPnl"])
        print("  size:\t", position["size"])
        print("  liq:\t", position["estimatedLiquidationPrice"])

def show_btc_markets(exchange):
    print("BTC markets:")
    for market in exchange.fetch_markets():
        id = market["id"]
        if id.startswith("BTC"):
            print(id)
            #pprint.pprint(market)

