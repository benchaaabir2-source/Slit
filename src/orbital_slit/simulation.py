import numpy as np
import matplotlib.pyplot as plt

# -----------------------
# PARAMÈTRES
# -----------------------
R = 1.0            # rayon de l'orbite
L = 5.0            # distance écran détecteur
a = 0.05           # largeur du passage
vx = 1.0           # vitesse du centre
omega = 2*np.pi    # vitesse angulaire
dt = 0.002         # pas de temps
N_centers = 200    # nombre de positions de centre
N_points = 50      # nombre de points par centre

# -----------------------
# SIMULATION
# -----------------------
def simulate_dynamic(D):
    hits = []

    # balayage du centre
    y_centers = np.linspace(D - R/2, D + R/2, N_centers)

    for yc in y_centers:
        for _ in range(N_points):
            # phase initiale aléatoire
            theta = np.random.uniform(0, 2*np.pi)

            # centre initial à gauche
            x_center = -2*R
            y = yc + R*np.sin(theta)
            x = x_center + R*np.cos(theta)

            # simulation temporelle
            while x < 0:
                theta += omega*dt
                x_center += vx*dt
                x_prev, y_prev = x, y
                x = x_center + R*np.cos(theta)
                y = yc + R*np.sin(theta)

                # passage du slit
                if x_prev < 0 <= x:
                    # interpolation pour trouver y exact au slit
                    frac = -x_prev/(x - x_prev)
                    theta_cross = theta - omega*dt + omega*dt*frac
                    y_cross = yc + R*np.sin(theta_cross)

                    if abs(y_cross) <= a/2:
                        # calcul de la trajectoire jusqu'à l'écran
                        vx_eff = vx - R*omega*np.sin(theta_cross)
                        vy_eff = R*omega*np.cos(theta_cross)
                        if vx_eff > 0:
                            t = L / vx_eff
                            y_hit = y_cross + vy_eff*t
                            hits.append(y_hit)
                    break

    return np.array(hits)

# -----------------------
# CAS À COMPARER
# -----------------------
D_small = 0.7   # D < R
D_large = 1.4   # D > R

hits_small = simulate_dynamic(D_small)
hits_large = simulate_dynamic(D_large)

# -----------------------
# PLOTS BRUTS
# -----------------------
plt.figure(figsize=(10,4))

plt.subplot(1,2,1)
plt.hist(hits_small, bins=200, density=True)
plt.title("D < R")
plt.xlabel("y impact")
plt.ylabel("densité")

plt.subplot(1,2,2)
plt.hist(hits_large, bins=200, density=True)
plt.title("D > R")
plt.xlabel("y impact")

plt.tight_layout()
plt.show()
