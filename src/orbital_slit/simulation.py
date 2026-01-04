import numpy as np

def simulate_dynamic(D, R=1.0, L=20.0, a=0.05, vx=0.05, omega=6*np.pi,
                     dt=0.001, N_centers=300, N_points=5):
    """
    Simulation fidèle au modèle original où centre et phase sont corrélés.
    - D : position centrale du balayage
    - R : rayon de l'orbite
    - L : distance écran détecteur
    - a : largeur du slit
    - vx : vitesse horizontale du centre
    - omega : vitesse angulaire de l'orbite
    - dt : pas de temps
    - N_centers : nombre de positions du centre dans le balayage
    - N_points : nombre de points simulés par centre
    Retour : array des y_impact
    """
    hits = []

    y_centers = np.linspace(D - R/2, D + R/2, N_centers)
    x_start = -5*R

    for yc in y_centers:
        for _ in range(N_points):
            theta = np.random.uniform(0, 2*np.pi)
            x_center = x_start
            x = x_center + R*np.cos(theta)
            y = yc + R*np.sin(theta)

            for _ in range(50000):  # max steps
                theta_prev = theta
                x_prev = x
                y_prev = y

                theta += omega*dt
                x_center += vx*dt
                x = x_center + R*np.cos(theta)
                y = yc + R*np.sin(theta)

                if x_prev < 0 <= x:
                    frac = -x_prev / (x - x_prev)
                    theta_cross = theta_prev + (theta - theta_prev) * frac
                    y_cross = yc + R*np.sin(theta_cross)

                    if abs(y_cross) <= a/2:
                        vx_eff = vx - R*omega*np.sin(theta_cross)
                        vy_eff = R*omega*np.cos(theta_cross)
                        if vx_eff > 1e-8:
                            t = L / vx_eff
                            y_hit = y_cross + vy_eff * t
                            hits.append(y_hit)
                    break

    return np.array(hits)
