import numpy as np

# At 1 keV
F = 3.5e-13   # erg s^-1 cm^-2 Hz^-1 
CGS_to_Jy = 1e23    # 1 Jy = 10^-23 erg s^-1 cm^-2 Hz^-1

f_Jy = F * CGS_to_Jy    # flux density in Jy
m_AB = -2.5 * np.log10(f_Jy / 3631)  # AB magnitude
print(f'Flux density = {f_Jy:.2e} Jy')
print(f'AB magnitude = {m_AB:.2f}')

# Convert flux from m_AB
f_AB_to_Jy = 3631 * pow(10, -0.4 * m_AB)   # flux in Jy
f_Jy_to_CGS = f_AB_to_Jy / CGS_to_Jy  # erg s^-1 cm^-2 Hz^-1 

h = 6.626e-27  # erg s
E_keV = 1.0  # 1 keV

F_p = f_Jy_to_CGS / (h * E_keV)
print(f'Photon flux = {F_p:.2e} photon cm^-2 s^-1 keV^-1')
