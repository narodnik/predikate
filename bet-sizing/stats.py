import math
import numpy as np
import pull

def stats(coin_id):
    # 1 hour ticks
    df = pull.pull("bitcoin", 30)
    df["r"] = np.log(df.price / df.price.shift(1))

    expect = df.r.mean()
    vol = df.r.var()
    return (expect, vol)

if __name__ == "__main__":
    expect, vol = stats("bitcoin")
    print(f"Expected mean: {expect}")
    print(f"Volatility: {vol}")
    
    print(f"Real mean: {math.e**expect - 1:.6f}")

