# Data
# S = 50, K = 50, t = 0, T = 0:5, sigma = 20%, and r = 1%.
# S = 50, K = 60, t = 0, T = 0:5, sigma = 20%, and r = 1%.
# S = 50, K = 50, t = 0, T = 1:0, sigma = 20%, and r = 1%.
# S = 50, K = 50, t = 0, T = 0:5, sigma = 30%, and r = 1%.
# S = 50, K = 50, t = 0, T = 0:5, sigma = 20%, and r = 2%.

def black_scholes(S, K, t, T, sigma, r):
  # Black Scholes Formula

  # Call Option
  # C(S,t) = SN(d1) - Ke^(-r(T - t)) * N(d2)

  # Put Option
  # P(S,t) = Ke^(-r(T - t)) * N(-d2) - SN(-d1)

  # d1 = (ln(S / K) + r(T - t)) / (sigma * √T) + ((1/2) * sigma * √T-t)
  # d2 = (ln(S / K) + r(T - t)) / (sigma * √T) - ((1/2) * sigma * √T-t)

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


  return None