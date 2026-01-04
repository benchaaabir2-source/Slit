import numpy as np

def simulate_correlated(D, R=1.0, L=5.0, a=0.05, vx=1.0, omega=2*np.pi,
                        dt=0.001, N_points=200_000):
    """
    Simulation d'un point sur orbite avec corrélation dynamique :
    - le centre avance dans le temps
    - la phase orbitale évolue avec le temps
    - le passage au slit se fait à un instant déterminé
    """
    hits = []

    # centres initiaux (tout à gauche)
    x_center = np.zeros(N_points) - 2*R
    y_center = np.random.uniform(D - R/2, D + R/2, N_points)
    
    # phase initiale
    theta = np.random.uniform(0, 2*np.pi, N_points)

    # positions orbites
    x = x_center + R * np.cos(theta)
    y = y_center + R * np.sin(theta)

    alive = np.ones(N_points, dtype=bool)  # points encore en course

    while alive.any():
        # avancer dans le temps
        theta[alive] += omega*dt
        x_center[alive] += vx*dt
        x[alive] = x_center[alive] + R * np.cos(theta[alive])
        y[alive] = y_center[alive] + R * np.sin(theta[alive])

        # vérifier passage du slit (x_prev < 0 <= x)
        crossing = alive & (x >= 0)
        if crossing.any():
            frac = - (x[~alive] if (~alive).any() else 0) / (x[crossing] - x[~alive].mean() if (~alive).any() else 1)
            y_cross = y[crossing]  # approximation pour l'instant de passage

            # sélection par slit
            mask_pass = np.abs(y_cross) <= a/2
            passed_idx = np.where(crossing)[0][mask_pass]

            # calcul impact écran
            vx_eff = vx - R*omega*np.sin(theta[passed_idx])
            vy_eff = R*omega*np.cos(theta[passed_idx])
            t = L / vx_eff
            y_hit = y[passed_idx] + vy_eff * t
            hits.extend(y_hit)

            # retirer les points passés
            alive[passed_idx] = False

        # retirer ceux qui ont dépassé le slit sans passer
        over = alive & (x > 0)
        alive[over] = False

    return np.array(hits)
