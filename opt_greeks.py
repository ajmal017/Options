import numpy as np
import scipy.stats as si


def delta_div(S, K, T, r, q, sigma, option):
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    if option == 'call':
        delta = np.exp(-q * T) * si.norm.cdf(d1, 0.0, 1.0)
    else:
        delta = -np.exp(-q * T) * si.norm.cdf(-d1, 0.0, 1.0)
    return delta


def theta_div(S, K, T, r, q, sigma, option):
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - q - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    if option == 'call':
        theta = -np.exp(-q * T) * (S * si.norm.cdf(d1, 0.0, 1.0) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(
            -r * T) * si.norm.cdf(d2, 0.0, 1.0) + q * S * np.exp(-q * T) * si.norm.cdf(d1, 0.0, 1.0)
    else:
        theta = -np.exp(-q * T) * (S * si.norm.cdf(d1, 0.0, 1.0) * sigma) / (2 * np.sqrt(T)) + r * K * np.exp(
            -r * T) * si.norm.cdf(-d2, 0.0, 1.0) - q * S * np.exp(-q * T) * si.norm.cdf(-d1, 0.0, 1.0)
    return theta


def gamma_div(S, K, T, r, q, sigma):
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    gamma = np.exp(-q * T) * si.norm.cdf(d1, 0.0, 1.0) / S * sigma * np.sqrt(T)

    return gamma


def vega_div(S, K, T, r, q, sigma):
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    vega = 1 / np.sqrt(2 * np.pi) * S * np.exp(-q * T) * np.exp(-d1 ** 2 * 0.5) * np.sqrt(T)

    return vega


def complete_greeks(S, K, T, r, q, sigma, option):
    delta = delta_div(S, K, T, r, q, sigma, option)
    gamma = gamma_div(S, K, T, r, q, sigma)
    vega = vega_div(S, K, T, r, q, sigma)
    theta = delta_div(S, K, T, r, q, sigma, option)
    return [delta, gamma, vega, theta]
