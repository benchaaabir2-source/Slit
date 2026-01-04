import matplotlib.pyplot as plt
from pathlib import Path
from orbital_slit.simulation import simulate_correlated

OUT = Path("artifacts")
OUT.mkdir(exist_ok=True)

# paramètres principaux
R = 1.0
L = 5.0
a = 0.05

# valeurs D à comparer
D_small = 0.7   # D < R
D_large = 1.4   # D > R

# simulation
hits_small = simulate_correlated(D_small, R=R, L=L, a=a)
hits_large = simulate_correlated(D_large, R=R, L=L, a=a)

# histogrammes sur le même plot
plt.figure(figsize=(10,5))
plt.hist(hits_small, bins=500, density=True, alpha=0.6, label="D<R")
plt.hist(hits_large, bins=500, density=True, alpha=0.6, label="D>R")
plt.title("Corrélation dynamique : comparaison D<R et D>R")
plt.xlabel("y impact")
plt.ylabel("densité")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "comparison_hist_dynamic.png")
plt.close()

print("Artifacts generated in /artifacts/comparison_hist_dynamic.png")
