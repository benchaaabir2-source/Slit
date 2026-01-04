# src/orbital_slit/export_artifacts.py
import matplotlib.pyplot as plt
from pathlib import Path
from orbital_slit.simulation import simulate_dynamic
import numpy as np
import json

OUT = Path("artifacts")
OUT.mkdir(exist_ok=True)

# ---- Paramètres (modifiables) ----
R = 1.0
# Choix de paramètres favorisant impacts étendus (épaule visible)
L = 20.0
a = 0.05
vx = 0.25
omega = 8 * 2 * np.pi   # angular speed
dt = 0.001
N_centers = 400
N_points = 1            # 1 trajectoire par centre = met en évidence la corrélation temporelle

# D values to compare
D_small = 0.7   # D < R
D_large = 1.4   # D > R

# ---- Simulation : mode "fixed" pour bien voir la sélection ----
hits_small, diag_small = simulate_dynamic(
    D_small, R=R, L=L, a=a, vx=vx, omega=omega, dt=dt,
    N_centers=N_centers, N_points=N_points, theta0_mode="fixed", theta0_value=0.0
)
hits_large, diag_large = simulate_dynamic(
    D_large, R=R, L=L, a=a, vx=vx, omega=omega, dt=dt,
    N_centers=N_centers, N_points=N_points, theta0_mode="fixed", theta0_value=0.0
)

# ---- 1) theta_cross vs center_y (all crossing phases, accepted and rejected) ----
plt.figure(figsize=(8,5))
plt.scatter(diag_large["center_y_all"], (diag_large["theta_cross_all"] % (2*np.pi)), s=4, alpha=0.6)
plt.xlabel("center_y (balayage)")
plt.ylabel("theta_cross (rad mod 2π)")
plt.title("theta_cross vs center_y (D>R) — toutes les crosses")
plt.tight_layout()
plt.savefig(OUT / "theta_vs_centery.png")
plt.close()

# ---- 2) histogramme des theta acceptées (phases favorisées) ----
plt.figure(figsize=(8,4))
if diag_large["theta_accepted"].size > 0:
    plt.hist(diag_large["theta_accepted"] % (2*np.pi), bins=80, density=True)
plt.xlabel("theta_accepted (rad mod 2π)")
plt.ylabel("density")
plt.title("Histogramme des phases acceptées (D>R)")
plt.tight_layout()
plt.savefig(OUT / "theta_accepted_hist.png")
plt.close()

# ---- 3) histogramme comparé des impacts (large range pour repérer épaule) ----
plt.figure(figsize=(10,5))
# choose range to capture large y shoulders, adjust if needed
ymin, ymax = -40, 40
plt.hist(hits_small, bins=400, range=(ymin,ymax), density=True, alpha=0.6, label=f"D<{R}")
plt.hist(hits_large, bins=400, range=(ymin,ymax), density=True, alpha=0.6, label=f"D>{R}")
plt.legend()
plt.xlabel("y impact")
plt.ylabel("density")
plt.title("Comparaison impacts — D<R vs D>R (mode dynamique)")
plt.tight_layout()
plt.savefig(OUT / "comparison_impacts_dynamic.png")
plt.close()

# ---- Save numeric summary ----
summary = {
    "params": {"R": R, "L": L, "a": a, "vx": vx, "omega": omega, "dt": dt, "N_centers": N_centers, "N_points": N_points},
    "D_small": {"D": D_small, "n_hits": int(hits_small.size)},
    "D_large": {"D": D_large, "n_hits": int(hits_large.size)},
}
with open(OUT / "summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Artifacts generated in artifacts/: theta_vs_centery.png, theta_accepted_hist.png, comparison_impacts_dynamic.png, summary.json")
