import numpy as np
from orbital_slit.analysis import gaussian_mle

def test_gaussian_fit():
    data = np.random.normal(1.0, 2.0, size=10000)
    mu, sigma = gaussian_mle(data)
    assert abs(mu - 1.0) < 0.1
    assert abs(sigma - 2.0) < 0.1
