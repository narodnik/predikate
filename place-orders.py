import random

total_amount = 0.25
number_orders = 10
start = 40215
end = 50000

increment = (end - start) / (number_orders - 1)
betsize = total_amount / number_orders

def randomize(value, percent_change):
    # This gives us a random number between [-1, 1]
    random_number = 2 * random.random() - 1
    delta = value * random_number * percent_change
    return value + delta

calc_total_amount = 0
average_price = 0

for i in range(number_orders):
    price = start + increment * i
    amount = betsize

    price = randomize(price, 0.0005)
    amount = randomize(amount, 0.2)
    average_price += price

    print("%i %.4f" % (price, amount))

    if i == (number_orders -1):
        amount = total_amount - calc_total_amount

    calc_total_amount += amount

average_price /= number_orders

# final amount should be the same as initial amount
print("Final amount: %.4f" % calc_total_amount)
print("Average price: %i" % average_price)

