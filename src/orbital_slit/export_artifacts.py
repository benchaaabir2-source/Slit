import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np                 # <-- c'était manquant
from orbital_slit.simulation import simulate_dynamic

OUT = Path("artifacts")
OUT.mkdir(exist_ok=True)

# Paramètres pour reproduire épaule 8–10
R = 1.0
L = 20.0
a = 0.05
vx = 0.05
omega = 6 * np.pi                # <-- np.pi OK maintenant
dt = 0.001
N_centers = 300
N_points = 5

# D<R et D>R
D_small = 0.7
D_large = 1.4

hits_small = simulate_dynamic(D_small, R=R, L=L, a=a, vx=vx, omega=omega, dt=dt,
                              N_centers=N_centers, N_points=N_points)
hits_large = simulate_dynamic(D_large, R=R, L=L, a=a, vx=vx, omega=omega, dt=dt,
                              N_centers=N_centers, N_points=N_points)

# Plot comparatif
plt.figure(figsize=(10,5))
plt.hist(hits_small, bins=400, range=(-5,15), density=True, alpha=0.6, label=f"D<{R}")
plt.hist(hits_large, bins=400, range=(-5,15), density=True, alpha=0.6, label=f"D>{R}")
plt.xlabel("y impact")
plt.ylabel("densité")
plt.title("Impacts D<R vs D>R — épaule visible (corrélation dynamique)")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "comparison_dynamic.png")
plt.close()

print("Artifact generated: artifacts/comparison_dynamic.png")
