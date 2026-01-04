import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from orbital_slit.analysis import gaussian_mle

OUT = Path("artifacts")
OUT.mkdir(exist_ok=True)

# fake data example (replace later with real simulation output)
data_small = np.random.normal(0.0, 1.0, 20_000)
data_large = np.random.normal(0.0, 1.8, 20_000)

mu_s, sigma_s = gaussian_mle(data_small)
mu_l, sigma_l = gaussian_mle(data_large)

# Save params
params = {
    "D<R": {"mu": mu_s, "sigma": sigma_s},
    "D>R": {"mu": mu_l, "sigma": sigma_l},
}

with open(OUT / "gaussian_params.json", "w") as f:
    json.dump(params, f, indent=2)

# Plot
def plot_gauss(data, mu, sigma, name):
    x = np.linspace(mu - 5*sigma, mu + 5*sigma, 500)
    y = (1/(sigma*np.sqrt(2*np.pi))) * np.exp(-(x-mu)**2/(2*sigma**2))

    plt.figure()
    plt.hist(data, bins=200, density=True, alpha=0.6)
    plt.plot(x, y)
    plt.title(name)
    plt.savefig(OUT / f"{name}.png")
    plt.close()

plot_gauss(data_small, mu_s, sigma_s, "gaussian_R_fixed_D_small")
plot_gauss(data_large, mu_l, sigma_l, "gaussian_R_fixed_D_large")

print("Artifacts generated in /artifacts")
