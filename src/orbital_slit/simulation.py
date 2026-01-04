#!/usr/bin/env python3
import math, json, time
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------
# Fonction de simulation dynamique (Option 2)
# -----------------------
def simulate_dynamic(D, R=0.5, L=2.0, a=0.05, vx=0.9, omega=3*math.pi, dt=0.002, N_centers=200, N_points=200):
    hits = []
    y_centers = np.linspace(D - R/2, D + R/2, N_centers)
    for yc in y_centers:
        for _ in range(N_points):
            theta = np.random.uniform(0, 2*math.pi)
            x_center = -2*R
            x = x_center + R*math.cos(theta)
            max_steps = int((abs(x) + 5*R) / (vx * dt) + 500)
            for step in range(max_steps):
                theta += omega*dt
                x_center += vx*dt
                x_prev = x
                x = x_center + R*math.cos(theta)
                if x_prev < 0 <= x:
                    denom = (x - x_prev)
                    frac = 0.5 if denom == 0 else max(0.0, min(1.0, -x_prev/denom))
                    theta_cross = theta - omega*dt + omega*dt*frac
                    y_cross = yc + R*math.sin(theta_cross)
                    if abs(y_cross) <= a/2.0:
                        vx_eff = vx - R*omega*math.sin(theta_cross)
                        vy_eff = R*omega*math.cos(theta_cross)
                        if vx_eff > 1e-8:
                            t_to_detector = L / vx_eff
                            y_hit = y_cross + vy_eff * t_to_detector
                            hits.append(y_hit)
                    break
    return np.array(hits)

# -----------------------
# Paramètres (modifie pour tester)
# -----------------------
R = 0.5          # rayon fixe
# Pour viser épaule ~8-10 commence par : L ~ 8..12 et/ou omega et/ou réduire vx
# Exemple initial :
L = 10.0         # distance écran — augmente pour tirer y vers de plus grandes valeurs
a = 0.05
vx = 0.9
omega = 3*math.pi  # essayer aussi omega = 4*pi ou 6*pi
dt = 0.002
N_centers = 300
N_points = 300    # augmente pour meilleure statistique

D_small = 0.7
D_large = 1.4

OUT = Path("artifacts")
OUT.mkdir(exist_ok=True, parents=True)

start = time.time()
hits_small = simulate_dynamic(D_small, R=R, L=L, a=a, vx=vx, omega=omega, dt=dt, N_centers=N_centers, N_points=N_points)
hits_large = simulate_dynamic(D_large, R=R, L=L, a=a, vx=vx, omega=omega, dt=dt, N_centers=N_centers, N_points=N_points)
end = time.time()

# Stats & percentiles
def stats(hits):
    if len(hits)==0:
        return {"n":0}
    return {
        "n": int(len(hits)),
        "mu": float(np.mean(hits)),
        "sigma": float(np.std(hits, ddof=0)),
        "percentiles": {p: float(v) for p,v in zip([1,5,10,25,50,75,90,95,99], np.percentile(hits, [1,5,10,25,50,75,90,95,99]))}
    }

res = {
    "params": {"R":R, "L":L, "a":a, "vx":vx, "omega":omega, "N_centers":N_centers, "N_points":N_points},
    "runtime_s": end-start,
    "D<R": stats(hits_small),
    "D>R": stats(hits_large)
}

# Save JSON
with open(OUT / "simulation_summary.json","w") as f:
    json.dump(res, f, indent=2)

# Plot overlay
plt.figure(figsize=(9,5))
bins = 300
if len(hits_small)>0:
    plt.hist(hits_small, bins=bins, density=True, alpha=0.5, label=f'D<R (n={len(hits_small)})')
if len(hits_large)>0:
    plt.hist(hits_large, bins=bins, density=True, alpha=0.5, label=f'D>R (n={len(hits_large)})')
plt.xlabel('y impact')
plt.ylabel('Density')
plt.title('Comparaison D<R vs D>R (dynamique)')
plt.legend()
plt.grid(True)
plt.savefig(OUT / "overlay_hist.png")
plt.close()

# Separate plots high-res
if len(hits_small)>0:
    plt.figure(figsize=(8,4))
    plt.hist(hits_small, bins=400, density=True)
    plt.title(f'D<R (n={len(hits_small)} mu={res["D<R"].get("mu",None):.3f} sigma={res["D<R"].get("sigma",None):.3f})')
    plt.xlabel('y impact')
    plt.ylabel('Density')
    plt.grid(True)
    plt.savefig(OUT / "hist_DltR.png")
    plt.close()

if len(hits_large)>0:
    plt.figure(figsize=(8,4))
    plt.hist(hits_large, bins=400, density=True)
    plt.title(f'D>R (n={len(hits_large)} mu={res["D>R"].get("mu",None):.3f} sigma={res["D>R"].get("sigma",None):.3f})')
    plt.xlabel('y impact')
    plt.ylabel('Density')
    plt.grid(True)
    plt.savefig(OUT / "hist_DgtR.png")
    plt.close()

print("Saved artifacts in:", OUT.resolve())
print("Summary JSON ->", OUT / "simulation_summary.json")
