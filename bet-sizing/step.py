import math
import numpy as np

def step(current_price, mean, var, delta_t):
    # Expected price: P e^(mu T)
    drift = mean * delta_t
    
    # Sample random x ~ N(0, 1)
    epsilon = np.random.normal()
    # Random brownian motion to combine with the drift
    noise = epsilon * math.sqrt(var * delta_t)
    
    # Convert from logspace
    next_price = current_price * math.e**(drift + noise)
    return next_price

if __name__ == "__main__":
    import stats

    # Look ahead 5 hours
    delta_t = 5
    # Mean and variance of lognormal price returns: log (P_i / P_{i - 1})
    mean, var = stats.stats("bitcoin")
    current_price = 46682
    next_price = step(current_price, mean, var, delta_t)
    print(f"Next price: {next_price}")

