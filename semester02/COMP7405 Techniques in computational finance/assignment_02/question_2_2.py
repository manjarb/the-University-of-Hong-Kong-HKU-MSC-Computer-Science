import numpy as np

# (2.2) Write a short program to numerically verify ρ(X,Z) = ρ


def generate_standard_normal_random_variable(size):
    # (a) write a standard normal random variable generator.
    return np.random.standard_normal(size=(size, 2))


def generate_Z(X, Y):
    # Please use 0.5 as the correlation ρ.
    p = 0.5
    # Z formula Z = ρX + ((√1-ρ^2) * Y)
    return (p * X) + (np.sqrt(1 - np.power(p, 2)) * Y)


def calculate_correlation_coefficient(X_list, Z_list):
    # snr_list = [[X, Y]]
    # Z_list = [Z]
    # Calculate ρ(X,Z)
    # ρ(X,Z) = Cov(X,Z) / √Var(X)Var(Z)
    # X_list = snr_list[:,0]
    return np.cov(X_list, Z_list, bias=True)[0][1] / np.sqrt(np.var(X_list) * np.var(Z_list))


def correlated_normal_random_variables():
    # (b) generate 200 samples of X and Y.
    # standard normal random variable size 200
    # snr = [[X,Y]]
    snr_list = generate_standard_normal_random_variable(200)

    # (c) generate the samples of Z using the formula and the samples of X and Y .
    Z_list = [generate_Z(snr[0], snr[1]) for snr in snr_list]

    # (d) calculate the sample correlation coefficient ρ(X,Z) based on the samples
    # of X and Z, and compare it with the theoretical value 0.5.
    X_list = snr_list[:, 0]

    print("p(X, Z): {}".format(calculate_correlation_coefficient(X_list, Z_list)))


correlated_normal_random_variables()
