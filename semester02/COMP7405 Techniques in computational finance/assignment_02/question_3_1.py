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


def black_scholes_vega(S, K, t, T, r, q, sigma):
    d1, d2 = calculate_d1_d2(S, K, t, T, r, q, sigma)
    time = T - t
    # Note that the formulas for ∂C(σ) / ∂σ and ∂P(σ) / ∂σ also need to change to:
    # ∂C(σ) / ∂σ = ∂P(σ) / ∂σ = Se^(-q(T - t)) * √T-t * N'(d1)
    return S * np.exp(-q * (time)) * np.sqrt(time) * norm.pdf(d1)


# (3.1)
# Implement the algorithm presented in Lecture 4 to calculate implied volatilities
# with the extended Black-Scholes formulas (1)-(2).
# ==========================================================================


def calculate_implied_volatility(S, K, t, T, r, q, option_type, C_true):
    time = T - t
    # The initial guess σ^ changes to:
    #
    # σ^ = √2|(lnS0 / K + (r - q)(T - t)) / T - t |
    sigma_hat = np.sqrt(2 * np.abs(np.log(S / K) + ((r - q) * (time))))
    tol = 1e-8
    nmax = 100
    sigma_diff = 1
    n = 1
    sigma = sigma_hat
    # C_true = black_scholes_call(S, K, t, T, r, q, sigma_true) if option_type == 'C' else black_scholes_put(S, K, t, T, r, q, sigma_true)

    while (sigma_diff >= tol and n < nmax):
        C = black_scholes_call(S, K, t, T, r, q, sigma) if option_type == 'C' else black_scholes_put(
            S, K, t, T, r, q, sigma)
        Cvega = black_scholes_vega(S, K, t, T, r, q, sigma)

        if Cvega == 0:
            return np.nan

        increment = (C - C_true) / Cvega
        sigma = sigma - increment
        n = n+1
        sigmadiff = abs(increment)

    return sigma
