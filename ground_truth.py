import numpy as np

# Constants
G = 6.6743e-11  # m^3 kg^-1 s^-2
M_earth = 5.9722e24  # kg
R_earth = 6.371e6  # m

h = 5.50e5  # m
r = R_earth + h  # m

# Velocity
v = np.sqrt(G * M_earth / r)  # m/s
l = 2 * np.pi * r  # m

# Orbital period
p = (l / v) / 60  # min 

print(f'{p:.2f} minutes')
