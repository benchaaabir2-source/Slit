import numpy as np

def simulate_dynamic(D, R=1.0, L=5.0, a=0.05, vx=1.0, omega=2*np.pi,
                     dt=0.002, N_centers=200, N_points=50):
    """
    Simulation dynamique d'un point sur orbite circulaire passant par un slit.
    Renvoie les positions y sur l'écran détecteur.
    """
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
                theta_prev = theta
                x_prev, y_prev = x, y

                theta += omega*dt
                x_center += vx*dt
                x = x_center + R*np.cos(theta)
                y = yc + R*np.sin(theta)

                # passage du slit
                if x_prev < 0 <= x:
                    frac = -x_prev/(x - x_prev)
                    theta_cross = theta_prev + (theta - theta_prev)*frac
                    y_cross = yc + R*np.sin(theta_cross)

                    if abs(y_cross) <= a/2:
                        vx_eff = vx - R*omega*np.sin(theta_cross)
                        vy_eff = R*omega*np.cos(theta_cross)
                        if vx_eff > 0:
                            t = L / vx_eff
                            y_hit = y_cross + vy_eff*t
                            hits.append(y_hit)
                    break

    return np.array(hits)
