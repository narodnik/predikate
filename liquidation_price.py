import math

entry_price = 9479.5
quantity = 10000
leverage = 10
funding_rate = 0.01 / 100 # 0.01%
taker_fee = 0.075 / 100
# As per the XBTUSD contract specification
maintenance_margin_requirement = 0.4 / 100

initial_margin_requirement = 1 / leverage

def calc_liquidation_price():
    print("====================================")
    print("LIQUIDATION PRICE")
    print("")
    order_value = abs(round(quantity * round(-100000000 / entry_price)))
    print("order_value:", order_value)

    cost = order_value * initial_margin_requirement
    print("cost:", cost)

    fee = round((order_value + cost) * taker_fee)
    print("fee:", fee)

    margin_requirement = (
        fee +
        order_value * min(initial_margin_requirement,
                          maintenance_margin_requirement + max(0, -funding_rate)))
    print("margin_requirement:", margin_requirement)

    # We round down but this is a negative number so we use ceil instead
    price = math.ceil(
        (-order_value - (cost + fee - margin_requirement)) / quantity)
    print("price:", price)

    liquidation_price = (-100000000 / price * 2) / 2
    print("liquidation_price:", liquidation_price)
    print("====================================")
    return liquidation_price

def calc_approx_liquidation_price():
    print("====================================")
    print("APPROX LIQUIDATION PRICE")
    print("")
    order_value = quantity / entry_price
    print("order_value:", order_value)

    cost = order_value * initial_margin_requirement
    print("cost:", cost)

    fee = (order_value + cost) * taker_fee
    print("fee:", fee)

    margin_requirement = (
        fee +
        order_value * maintenance_margin_requirement)
    print("margin_requirement:", margin_requirement)

    # We round down but this is a negative number so we use ceil instead
    price = \
        (order_value + (cost + fee - margin_requirement)) / quantity
    print("price:", price)

    liquidation_price = 1 / price
    print("liquidation_price:", liquidation_price)
    print("====================================")
    return liquidation_price

def calc_super_approx_liquidation_price():
    print("====================================")
    print("SUPER APPROX LIQUIDATION PRICE")
    print("")
    liquidation_price = entry_price * leverage / (leverage + 1)
    print("liquidation_price:", liquidation_price)
    print("====================================")
    return liquidation_price

real = calc_liquidation_price()
approx = calc_approx_liquidation_price()
super_approx = calc_super_approx_liquidation_price()

print("")
print("ERRORS:")
print("")
print("approx: %s %%" % abs(100 * (real - approx) / real))
print("super_approx: %s %%" % abs(100 * (real - super_approx) / real))

