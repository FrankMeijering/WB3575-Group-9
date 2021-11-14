import numpy as np
import matplotlib.pyplot as plt

# ------------------------ CONSTANTS AND VARIABLES ----------------------------
# Constants
kappa_air = 1.4     # Ratio of specific heats
p_atm = 101325      # Pressure in Pascal
R_air = 287.06      # Specific gas constant in J/kg.K
cp_air = R_air/(1-1/kappa_air)   # Specific heat at constant pressure of air in J/kg.K

# Variables
T_atm = 293.15      # Temperature in Kelvin
p2_int = 2.5e5        # Integer value of pressure after compressor (regulated with valve)

# ----------------------------- CALCULATIONS ----------------------------------
# State 'atm' is before the compressor
# State '2' is after the compressor
step = 0.05
eta_comp_lst = np.arange(0.2, 1.+step, step)
p2 = p2_int*np.ones(len(eta_comp_lst))   # Pa
T2 = T_atm*(1+(1/eta_comp_lst)*((p2_int/p_atm)**((kappa_air-1)/kappa_air)-1))    # K
W_sp_comp = cp_air*(T2-T_atm*np.ones(len(T2)))   # J/kg

# ------------------------------ PLOTTING -------------------------------------
fig = plt.figure()
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)

ax1.plot(eta_comp_lst*100, T2-273.15, label=r'$T_2$')
ax1.set_xlabel(r'$\eta_{is, comp}$ [%]')
ax1.set_ylabel(r'$T_2$ [$\degree$C]')
ax1.legend()

ax2.plot(eta_comp_lst*100, p2/1e5, label=r'$p_2$')
ax2.set_xlabel(r'$\eta_{is, comp}$ [%]')
ax2.set_ylabel(r'$p_2$ [bar]')
ax2.legend()

ax3.plot(eta_comp_lst*100, W_sp_comp/1e6, label=r'$W_{sp, comp}$')
ax3.set_xlabel(r'$\eta_{is, comp}$ [%]')
ax3.set_ylabel(r'$W_{sp, comp}$ [MJ/kg]')
ax3.legend()

fig.tight_layout()
plt.show()
