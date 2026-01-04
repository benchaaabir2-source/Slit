import numpy as np
import matplotlib.pyplot as plt
from orbital_slit.simulation import simulate_collect
from orbital_slit.analysis import gaussian_mle, kde_silverman
from orbital_slit.plotting import plot_distribution

R = 0.5
D_values = {"D < R": 0.2, "D > R": 1.2}

x_grid = np.linspace(-6, 6, 1000)

for label, D in D_values.items():
    data = simulate_collect(R=R, D=D)
    mu, sigma = gaussian_mle(data)
    kde = kde_silverman(data, x_grid)
    plot_distribution(data, mu, sigma, x_grid, kde, label)

plt.legend()
plt.xlabel("y impact")
plt.ylabel("Density")
plt.title("Impact distributions – R fixed, D variable")
plt.show()
