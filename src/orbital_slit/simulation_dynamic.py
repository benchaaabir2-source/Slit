import numpy as np

def simulate_orbit(D, R, L=5.0, a=0.05, vx=1.0, omega=2*np.pi, N=200_000, dt=0.001):
    """
    Simulation avec orbite dynamique et balayage du centre.
    
    D : position centrale du slit
    R : rayon de l’orbite
    L : distance écran détecteur
    a : largeur du passage
    vx : vitesse du centre
    omega : vitesse angulaire orbitale
    N : nombre de points simulés
    dt : pas de temps pour orbite
    """
    hits = []

    # balayage du centre (D - R/2 -> D + R/2)
    y_centers = np.random.uniform(D - R/2, D + R/2, N)
    theta = np.random.uniform(0, 2*np.pi, N)

    # simulation point par point (méthode discrète)
    for i in range(N):
        y_c = y_centers[i]
        th = theta[i]
        x = -2*R  # départ bien à gauche
        y = y_c + R*np.sin(th)

        # petite boucle temps pour atteindre x = 0
        while x < 0:
            th_prev = th
            x_prev = x
            x += vx*dt
            th += omega*dt
            y_curr = y_c + R*np.sin(th)

            # passage x=0
            if x_prev < 0 <= x:
                frac = -x_prev/(x - x_prev)
                th_cross = th_prev + omega*frac*dt
                y_cross = y_c + R*np.sin(th_cross)

                # condition slit
                if abs(y_cross) <= a/2:
                    vx_eff = vx - R*omega*np.sin(th_cross)
                    vy_eff = R*omega*np.cos(th_cross)
                    if vx_eff > 0:
                        t = L / vx_eff
                        y_hit = y_cross + vy_eff*t
                        hits.append(y_hit)
                break

    return np.array(hits)
