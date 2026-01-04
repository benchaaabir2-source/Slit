import matplotlib.pyplot as plt
import numpy as np

def plot_distribution(data, mu, sigma, kde_x, kde_y, label):
    plt.hist(data, bins=120, density=True, alpha=0.4, label=f"{label} hist")
    plt.plot(kde_x, kde_y, label=f"{label} KDE", linewidth=2)
    gauss = (
        1 / (sigma * np.sqrt(2 * np.pi))
        * np.exp(-0.5 * ((kde_x - mu) / sigma) ** 2)
    )
    plt.plot(kde_x, gauss, "--", label=f"{label} Gaussian")
