import numpy as np
import matplotlib.pyplot as plt

# ------------------------ CONSTANTS AND VARIABLES ----------------------------
# Constants
kappa_air = 1.4     # Ratio of specific heats
p_atm = 101325      # Pressure in Pascal
R_uni = 8.31446     # Universal gas constant in J/mol.K

# Variables
T_atm = 288.15      # Temperature in Kelvin
eta_comp = 0.5      # Isentropic compressor efficiency
M = 0               # Free stream Mach number
p_ratio_comp = 5    # Pressure ratio of compressor

# ----------------------------- CALCULATIONS ----------------------------------
# State 'atm' is before the compressor
# State '2' is after the compressor
step = 0.05
eta_comp_lst = np.arange(0.4, 0.7+step, step)
p2 = p_atm*p_ratio_comp*np.ones(len(eta_comp_lst))
T2 = T_atm*(1+(1/eta_comp_lst)*(p_ratio_comp**((kappa_air-1)/kappa_air)-1))

fig = plt.figure()
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)
ax1.plot(eta_comp_lst*100, T2, label='T2')
ax2.plot(eta_comp_lst*100, p2, label='p2')
ax1.set_xlabel('Isentropic compressor efficiency [%]')
ax1.set_ylabel('T2 [K]')
ax2.set_xlabel('Isentropic compressor efficiency [%]')
ax2.set_ylabel('p2 [Pa]')
ax1.legend()
ax2.legend()
plt.show()
