import numpy as np
import matplotlib.pyplot as plt

# ------------------------ CONSTANTS AND VARIABLES ----------------------------
# Constants
kappa_air = 1.4     # Ratio of specific heats
p_atm = 101325      # Pressure in Pascal
R_uni = 8.31446     # Universal gas constant in J/mol.K
R_air = 287.06      # Specific gas constant in J/kg.K
cp_air = R_air/(1-1/kappa_air)   # Specific heat at constant pressure of air in J/kg.K

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
W_sp_comp = cp_air*(T2-T_atm*np.ones(len(T2)))


# ------------------------------ PLOTTING -------------------------------------
fig = plt.figure()
ax1 = fig.add_subplot(1, 3, 1)
ax2 = fig.add_subplot(1, 3, 2)
ax3 = fig.add_subplot(1, 3, 3)

ax1.plot(eta_comp_lst*100, T2, label=r'$T_2$')
ax1.set_xlabel(r'$\eta_{is, comp}$ [%]')
ax1.set_ylabel(r'$T_2$ [K]')
ax1.legend()

ax2.plot(eta_comp_lst*100, p2, label=r'$p_2$')
ax2.set_xlabel(r'$\eta_{is, comp}$ [%]')
ax2.set_ylabel(r'$p_2$ [Pa]')
ax2.legend()

ax3.plot(eta_comp_lst*100, W_sp_comp, label=r'$W_{sp, comp}$')
ax3.set_xlabel(r'$\eta_{is, comp}$ [%]')
ax3.set_ylabel(r'$W_{sp, comp}$ [J/kg]')
ax3.legend()

plt.show()
