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

total_pnl = 0

for position in exchange.fetch_positions():
    if position["size"] == 0:
        continue

    #pprint.pprint(position)
    id = position["future"]
    print(id)
    pnl = position["realizedPnl"]
    total_pnl += pnl
    print("  PNL:\t", pnl)
    print("  size:\t", position["size"])
    liquidation = position["estimatedLiquidationPrice"]
    print("  liq:\t", liquidation)

    ticker = exchange.fetch_ticker(id)
    last = ticker["last"]
    print("  last price:\t", last)
    print("  risk:\t %.2f%%" % (
        100 * (1 - ((last - liquidation) / last))))

print()
print("Total PNL:", total_pnl)

def show_btc_markets(exchange):
    print("BTC markets:")
    for market in exchange.fetch_markets():
        id = market["id"]
        if id.startswith("BTC"):
            print(id)
            #pprint.pprint(market)

