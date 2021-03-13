import numpy as np
from scipy.stats import norm

# σ = sigma
# δ = delta


def calculate_d1_d2(S, K, t, T, r, q, sigma):
    time = T - t
    lnSK = np.log(S / K)
    rate = r - q
    denominator = sigma * (np.sqrt(time))
    plus_sigma = (1 / 2) * sigma * np.sqrt(time)

    # d1 = ((ln(S / K) + (r - q)(T - t)) / (sigma * √T-t)) + ((1/2) * sigma * √T-t)
    d1 = ((lnSK + (rate * time)) / denominator) + plus_sigma

    # d1 = ((ln(S / K) + (r - q)(T - t)) / (sigma * √T-t)) - ((1/2) * sigma * √T-t)
    d2 = ((lnSK + (rate * time)) / denominator) - plus_sigma

    return d1, d2


def black_scholes_call(S, K, t, T, r, q, sigma):
    time = T - t
    d1, d2 = calculate_d1_d2(S, K, t, T, r, q, sigma)
    # Call Option
    # C(S,t) = Se^(-q(T - t))N(d1) - Ke^(-r(T - t)) * N(d2)
    return (S * np.exp(-q * (time)) * norm.cdf(d1)) - ((K * np.exp(-r * (time))) * norm.cdf(d2))


def black_scholes_put(S, K, t, T, r, q, sigma):
    time = T - t
    d1, d2 = calculate_d1_d2(S, K, t, T, r, q, sigma)
    # Call Option
    # P(S,t) = Ke^(-r(T - t)) * N(-d2) - Se^(-q(T - t))N(-d1)
    return ((K * np.exp(-r * (time))) * norm.cdf(-d2)) - (S * np.exp(-q * (time)) * norm.cdf(-d1))


def call_put_parity(S, K, t, T, r, q):
    # Se^(-q(T - t)) - Ke^(-r(T - t))
    time = T - t
    return (S * np.exp(-q * (time))) - (K * np.exp(-r * (time)))