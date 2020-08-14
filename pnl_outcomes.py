import matplotlib.pyplot as plt

start_price = 9270
n_contracts = 85000
margin = 2.22

def pnl(exit_price):
    rpnl = n_contracts * (1/start_price - 1/exit_price) * exit_price
    margin_profit = margin * (exit_price - start_price)
    return rpnl + margin_profit

xvalues = list(range(9500, 15000, 100))
yvalues = [pnl(x) for x in xvalues]

#xvalues, yvalues = simulate_pnls()

plt.style.use('dark_background')

plt.title("PNL at each price point in USD (including margin profit)")

ax = plt.gca()
ax.yaxis.set_label_position("right")
ax.yaxis.tick_right()
ax.grid(which='major', color='#666666', linestyle=':')
ax.minorticks_on()
ax.grid(which='minor', color='#999999', linestyle='-', alpha=0.2)

ax.plot(xvalues, yvalues)

plt.legend()
plt.show()
