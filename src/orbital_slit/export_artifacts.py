import matplotlib.pyplot as plt
from pathlib import Path
from orbital_slit.simulation_dynamic import simulate_orbit

OUT = Path("artifacts")
OUT.mkdir(exist_ok=True)

# Paramètres
R = 1.0
cases = {"D<R": 0.7, "D>R": 1.4}
L = 5.0
a = 0.05

for label, D in cases.items():
    hits = simulate_orbit(D=D, R=R, L=L, a=a, N=50_000)  # 50k pour CI rapide
    plt.figure(figsize=(6,4))
    plt.hist(hits, bins=400, density=True, alpha=0.7)
    plt.title(f"Orbital slit {label}")
    plt.xlabel("y impact")
    plt.ylabel("Density")
    plt.tight_layout()
    plt.savefig(OUT/f"{label}.png")
    plt.close()

print("Artifacts generated:", list(OUT.iterdir()))
