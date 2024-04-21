#!/usr/bin/env python

"""
iner_osci.py

2D Idealized Inertial Oscillation Solver

Sandy Herho <sandy.herho@email.ucr.edu>

04/21/2024
"""

import numpy as np

# Constants
pi = np.pi
freq = -2 * pi / (24 * 3600)
f = 2 * freq
dt = 6 * 24 * 3600 / 120
alpha = f * dt
beta = 0.25 * alpha * alpha
ntot = 120
uzero = 0.05
vzero = 0.05
initial_conditions = {
    'u': 0.1, 'v': 0.0, 'x': 0.0, 'y': 0.0
}

def update_positions_and_velocities(u, v, du, dv):
    ustar = u + du
    vstar = v + dv
    un = (ustar * (1 - beta) + alpha * vstar) / (1 + beta)
    vn = (vstar * (1 - beta) - alpha * ustar) / (1 + beta)
    return un, vn

def write_outputs(file, x, y, time):
    file.write(f"{x:.6f} {y:.6f} {time:.2f}\n")

def simulate(mode: int):
    conditions = np.array([initial_conditions['u'], initial_conditions['v'], initial_conditions['x'], initial_conditions['y']])
    filename = f'output_py_{mode}.txt'
    
    with open(filename, 'w') as file:
        file.write(f"{freq} {dt} {ntot}\n")
        
        for n in range(1, ntot + 1):
            time = n * dt
            du, dv = (0.0, -0.3 if n == 40 else 0.1 if n == 80 else 0.0)
            
            if mode == 1:
                u, v = update_positions_and_velocities(conditions[0], conditions[1], du, dv)
            else:
                u = np.cos(alpha) * conditions[0] + np.sin(alpha) * conditions[1] + du
                v = np.cos(alpha) * conditions[1] - np.sin(alpha) * conditions[0] + dv
            
            x = conditions[2] + dt * (u + uzero) / 1000
            y = conditions[3] + dt * (v + vzero) / 1000
            conditions = np.array([u, v, x, y])
            
            write_outputs(file, x, y, time)

def main():
    simulate(mode=1)
    simulate(mode=2)

if __name__ == "__main__":
    main()

