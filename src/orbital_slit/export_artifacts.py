import matplotlib.pyplot as plt
from pathlib import Path
from orbital_slit.simulation_dynamic import simulate_orbit
import re

OUT = Path("artifacts")
OUT.mkdir(exist_ok=True)

# Paramètres
R = 1.0
cases = {"D_lt_R": 0.7, "D_gt_R": 1.4}  # safe filenames
L = 5.0
a = 0.05

for label, D in cases.items():
    hits = simulate_orbit(D=D, R=R, L=L, a=a, N=50_000)  # 50k points pour CI rapide

    # Nettoyage du label pour être safe
    safe_label = re.sub(r'[<>:"|?*]', '_', label)

    plt.figure(figsize=(6,4))
    plt.hist(hits, bins=400, density=True, alpha=0.7)
    plt.title(f"Orbital slit {label}")
    plt.xlabel("y impact")
    plt.ylabel("Density")
    plt.tight_layout()
    plt.savefig(OUT/f"{safe_label}.png")
    plt.close()

print("Artifacts generated:", list(OUT.iterdir()))
