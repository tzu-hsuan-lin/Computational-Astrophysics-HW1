import numpy as np

# Constants
G = 6.6743e-11  # m^3 kg^-1 s^-2
M_earth = 5.972e24  # kg
R_earth = 6371e3  # m

h = 550e3  # m
r = R_earth + h  # m

# Velocity
v = np.sqrt(G * M_earth / r)  # m/s
l = 2 * np.pi * r  # m

# Orbital period
p = (l / v) / 60  # min 

print(p,f'minute')
