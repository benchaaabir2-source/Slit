import math
import random
import numpy as np
import pandas as pd

def simulate_collect(
    R,
    D,
    slit_width=0.05,
    L=1.0,
    v_center=0.6,
    omega=4*math.pi,
    N_trials=2000,
    n_centers=50,
    dt=0.003,
):
    centers_y = np.linspace(D - R/2, D + R/2, n_centers)
    hits = []

    for cy in centers_y:
        for _ in range(N_trials):
            theta = random.random() * 2 * math.pi
            cx = -2 * max(R, 1.0)
            x_prev = cx + R * math.cos(theta)
            theta_prev = theta

            for _ in range(2000):
                cx += v_center * dt
                theta += omega * dt
                x_curr = cx + R * math.cos(theta)

                if x_prev < 0 <= x_curr:
                    frac = -x_prev / (x_curr - x_prev)
                    theta_cross = theta_prev + omega * frac * dt
                    y_cross = cy + R * math.sin(theta_cross)

                    if abs(y_cross) <= slit_width / 2:
                        vx = v_center - R * omega * math.sin(theta_cross)
                        vy = R * omega * math.cos(theta_cross)
                        if vx > 0:
                            t = L / vx
                            y_hit = y_cross + vy * t
                            hits.append(y_hit)
                    break

                x_prev = x_curr
                theta_prev = theta

    return np.array(hits)
