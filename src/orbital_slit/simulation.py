import numpy as np
import matplotlib.pyplot as plt

# -----------------------
# PARAMÈTRES PHYSIQUES
# -----------------------
R = 1.0              # rayon de l’orbite (FIXE)
L = 5.0              # distance écran détecteur
a = 0.05             # largeur du passage
vx = 1.0             # vitesse horizontale du centre
omega = 2 * np.pi    # vitesse angulaire
N = 200_000          # nombre de points

# -----------------------
# FONCTION DE SIMULATION
# -----------------------
def simulate(D):
    impacts = []

    # balayage du centre (TA règle)
    y_centers = np.random.uniform(
        D - R/2,
        D + R/2,
        N
    )

    # phase orbitale aléatoire
    theta = np.random.uniform(0, 2*np.pi, N)

    # position au passage x = 0
    y_pass = y_centers + R * np.sin(theta)

    # condition de passage
    mask = np.abs(y_pass) <= a/2

    # vitesses transverses au passage
    vy = R * omega * np.cos(theta[mask])
    vx_eff = vx - R * omega * np.sin(theta[mask])

    # élimination des trajectoires rétrogrades
    mask2 = vx_eff > 0
    y_pass = y_pass[mask][mask2]
    vy = vy[mask2]
    vx_eff = vx_eff[mask2]

    # impact sur l’écran détecteur
    t = L / vx_eff
    y_hit = y_pass + vy * t

    return y_hit

# -----------------------
# CAS À COMPARER
# -----------------------
D_small = 0.7   # D < R
D_large = 1.4   # D > R

hits_small = simulate(D_small)
hits_large = simulate(D_large)

# -----------------------
# PLOTS (BRUTS)
# -----------------------
plt.figure(figsize=(10,4))

plt.subplot(1,2,1)
plt.hist(hits_small, bins=400, density=True)
plt.title("D < R")
plt.xlabel("y impact")
plt.ylabel("densité")

plt.subplot(1,2,2)
plt.hist(hits_large, bins=400, density=True)
plt.title("D > R")
plt.xlabel("y impact")

plt.tight_layout()
plt.show()
