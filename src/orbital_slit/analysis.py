import numpy as np
import math

def gaussian_mle(data):
    mu = np.mean(data)
    sigma = np.sqrt(np.mean((data - mu) ** 2))
    return mu, sigma

def kde_silverman(data, x):
    n = len(data)
    std = np.std(data)
    h = 1.06 * std * n ** (-1 / 5)
    return np.sum(
        np.exp(-0.5 * ((x[:, None] - data[None, :]) / h) ** 2),
        axis=1
    ) / (n * h * math.sqrt(2 * math.pi))
