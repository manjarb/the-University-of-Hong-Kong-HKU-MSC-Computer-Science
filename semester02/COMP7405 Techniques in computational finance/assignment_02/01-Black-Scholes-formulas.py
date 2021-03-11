import numpy as np
from scipy.stats import norm


# 1. (2 marks) Implement the Black-Scholes formulas for C(S; t) and P(S; t),
# and calculate the values of both call and put options with following parameters:
# Data
# S = 50, K = 50, t = 0, T = 0:5, sigma = 20%, and r = 1%.
# S = 50, K = 60, t = 0, T = 0:5, sigma = 20%, and r = 1%.
# S = 50, K = 50, t = 0, T = 1:0, sigma = 20%, and r = 1%.
# S = 50, K = 50, t = 0, T = 0:5, sigma = 30%, and r = 1%.
# S = 50, K = 50, t = 0, T = 0:5, sigma = 20%, and r = 2%.
data = [
    {
        "S": 50,
        "K": 50,
        "t": 0,
        "T": 0.5,
        "sigma": 0.2,
        "r": 0.01
    },
    {
        "S": 50,
        "K": 60,
        "t": 0,
        "T": 0.5,
        "sigma": 0.2,
        "r": 0.01
    },
    {
        "S": 50,
        "K": 50,
        "t": 0,
        "T": 1,
        "sigma": 0.2,
        "r": 0.01
    },
    {
        "S": 50,
        "K": 50,
        "t": 0,
        "T": 0.5,
        "sigma": 0.3,
        "r": 0.01
    },
    {
        "S": 50,
        "K": 50,
        "t": 0,
        "T": 0.5,
        "sigma": 0.2,
        "r": 0.02
    },
]

# σ = sigma
# δ = delta

# S = Current stock price
# N(d1) and N(d2) = Cumulative density function
# K = Exercise price
# r = Annualised risk free rate
# d = Annual dividend yield of underlying stock
# T = Time to expiry
# ln(S / X) = Natural logarithmic value of (S / X)
# e = 2.71828
# delta = Annual dividend yield of underlying stock
# sigma = Annualised standard deviation of share returns or Volatility

def d1(S, K, t, T, r, sigma):
    # d1 = ((ln(S / K) + (r + (sigma^2 / 2)) * (T - t)) / (sigma * √T-t)
    time = T - t
    lnSK = np.log(S / K)
    rate = (r + (np.power(sigma, 2) / 2)) * (time)
    denominator = sigma * (np.sqrt(time))
    return (lnSK + rate) / denominator


def d2(S, K, t, T, r, sigma):
    # d2 = d1 - sigma * √T-t
    return d1(S, K, t, T, r, sigma) - (sigma * np.sqrt(T - t))


def black_scholes_call(S, K, t, T, r, sigma):
    # Call Option
    # C(S,t) = SN(d1) - Ke^(-r(T - t)) * N(d2)
    return (S * norm.cdf(d1(S, K, t, T, r, sigma))) - ((K * np.exp(-r * (T - t))) * norm.cdf(d2(S, K, t, T, r, sigma)))


def black_scholes_put(S, K, t, T, r, sigma):
    # Put Option
    # P(S,t) = Ke^(-r(T - t)) * N(-d2) - SN(-d1)
    return K * np.exp(-r * (T - t)) * norm.cdf(-(d2(S, K, t, T, r, sigma))) - (S * norm.cdf(-(d1(S, K, t, T, r, sigma))))


for stock in data:
    print("Stock data: {}".format(stock))
    S = stock["S"]
    K = stock["K"]
    t = stock["t"]
    T = stock["T"]
    r = stock["r"]
    sigma = stock["sigma"]
    print("Call option price: {}".format(
        black_scholes_call(S, K, t, T, r, sigma)))
    print("Put option price: {}".format(
        black_scholes_put(S, K, t, T, r, sigma)))
