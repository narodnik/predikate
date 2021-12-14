import stats
import step

mean, var = stats.stats("bitcoin")
original_price = 46682

# I assume mean flips
mean = -mean

# Position size in BTC
position = 1
# Margin also in BTC
margin = 0.1
assert margin > 0

# Lets do 20 days until just after new year
hours = 20 * 24

pnl_outcomes = []

for _ in range(1000):
    price = original_price
    state = "RUNNING"
    for _ in range(hours):
        price = step.step(price, mean, var, 1)
        pnl = position * (price - original_price)
        # convert pnl to BTC
        pnl_btc = pnl / price
        if pnl_btc + margin < 0:
            state = "LIQ"
            break

    if state == "RUNNING":
        pnl_outcomes.append(pnl)
    elif state == "LIQ":
        margin_usd = margin * price
        pnl_outcomes.append(-margin_usd)
    else:
        assert False

#print(pnl_outcomes)
print(sum(pnl_outcomes) / len(pnl_outcomes))

