import numpy as np

# At 1 keV
F_nu = 3.5e-13   # erg s^-1 cm^-2 Hz^-1 
CGS_to_Jy = 1e23    # 1 Jy = 10^-23 erg s^-1 cm^-2 Hz^-1

F_Jy = F_nu * CGS_to_Jy    # flux density in Jy
m_AB = -2.5 * np.log10(F_Jy / 3631)  # AB magnitude
print(f'Flux density = {F_Jy:.2E} Jy')
print(f'AB magnitude = {m_AB:.2f}')

# Convert flux density from m_AB
F_AB_to_Jy = 3631 * pow(10, -0.4 * m_AB)   # Jy
F_Jy_to_CGS = F_AB_to_Jy / CGS_to_Jy  # erg s^-1 cm^-2 Hz^-1 

# Photon flux per keV
h = 6.626e-27  # erg s
E_keV = 1.0  # 1 keV

N_E = F_Jy_to_CGS / (h * E_keV)
print(f'Photon flux = {N_E:.2E} photon cm^-2 s^-1 keV^-1')
