# src/orbital_slit/simulation.py
import numpy as np

def simulate_dynamic(
    D,
    R=1.0,
    L=20.0,
    a=0.05,
    vx=0.25,
    omega=8 * 2 * np.pi,
    dt=0.001,
    N_centers=400,
    N_points=1,
    theta0_mode="fixed",  # "fixed" or "random"
    theta0_value=0.0,     # used if theta0_mode=="fixed"
):
    """
    Simulation dynamique d'un point sur orbite circulaire passant par un slit.
    - D : position y du centre du balayage (le slit est centré en y=0, le centre balaie autour de D)
    - R : rayon de l'orbite
    - L : distance écran détecteur (plus L grand -> impacts plus étendus)
    - a : largeur du slit
    - vx: vitesse du centre (en x)
    - omega: vitesse angulaire (rad/s)
    - dt: pas de temps
    - N_centers: nombre de positions du centre dans le balayage
    - N_points: nombre de trajectoires simulées par centre (phase initiale)
    - theta0_mode: "fixed" => même theta0 pour tous (met en évidence la corrélation),
                   "random" => theta0 aléatoire (moyennation)
    - theta0_value: la valeur de theta0 si mode "fixed"
    Retour:
      hits: array des y_impact
      diagnostics: dict contenant arrays pour tracer theta_cross vs center_y et theta_accepted
    """
    hits = []
    theta_cross_list = []
    center_y_list = []
    theta_accepted = []

    # balayage du centre (centre_y déplacé linéairement)
    y_centers = np.linspace(D - R/2, D + R/2, N_centers)

    # longueur initiale en x (centre initial à gauche)
    x_center_start = -5.0 * max(R, 1.0)

    for yc in y_centers:
        for _ in range(N_points):
            # initial phase selon le mode
            if theta0_mode == "fixed":
                theta = float(theta0_value)
            else:
                theta = np.random.uniform(0.0, 2*np.pi)

            # initialisation position du centre et du point
            x_center = x_center_start
            x = x_center + R * np.cos(theta)
            y = yc + R * np.sin(theta)

            # on evolve jusqu'au passage x>=0 ou jusqu'à un nombre d'itérations maxi
            max_steps = int( (abs(x_center_start) + 5.0*R) / (vx * dt) ) + 1000
            step = 0
            crossed = False
            while x < 0 and step < max_steps:
                step += 1
                theta_prev = theta
                x_prev = x

                # integrate
                theta = theta + omega * dt
                x_center = x_center + vx * dt
                x = x_center + R * np.cos(theta)
                y = yc + R * np.sin(theta)

                if x_prev < 0 <= x:
                    # interpolation fraction to find exact crossing point
                    if (x - x_prev) == 0:
                        frac = 0.5
                    else:
                        frac = -x_prev / (x - x_prev)
                    theta_cross = theta_prev + (theta - theta_prev) * frac
                    y_cross = yc + R * np.sin(theta_cross)

                    # diagnostics store
                    theta_cross_list.append(theta_cross % (2*np.pi))
                    center_y_list.append(yc)

                    if abs(y_cross) <= a/2.0:
                        vx_eff = vx - R * omega * np.sin(theta_cross)
                        vy_eff = R * omega * np.cos(theta_cross)
                        # store accepted theta
                        theta_accepted.append(theta_cross % (2*np.pi))
                        if vx_eff > 1e-9:
                            t_to_detector = L / vx_eff
                            y_hit = y_cross + vy_eff * t_to_detector
                            hits.append(y_hit)
                    crossed = True
                    break

            # if never crossed, we skip

    diagnostics = {
        "theta_cross_all": np.array(theta_cross_list),
        "center_y_all": np.array(center_y_list),
        "theta_accepted": np.array(theta_accepted),
    }
    return np.array(hits), diagnostics
