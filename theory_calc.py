import numpy as np
import matplotlib.pyplot as plt
from tools import cp_air, kappa_air, p_atm

# ------------------------ CONSTANTS AND VARIABLES ----------------------------
T_atm = 292.15   # Temperature in Kelvin (on average 19 degrees Celsius)
p_high = 2.5e5   # High pressure (after compressor, before turbine) in [Pa]

# ----------------------------- CALCULATIONS ----------------------------------
# Define x-axis of efficiencies
step = 0.01
eta_comp_lst = np.arange(0.1, 1.+step, step)

# Specific work equation is from the adiabatic energy balance (Q=0)
# T_atm and p_atm are before the compressor, T2 and p_high are after the compressor
T2_comp = T_atm*(1+(1/eta_comp_lst)*((p_high/p_atm)**((kappa_air-1)/kappa_air)-1))    # [K]
W_sp_comp = cp_air*(T2_comp-T_atm*np.ones(len(T2_comp)))   # [J/kg] Work done *ON* compressor

# T_atm and p_high are before the turbine, T2 and p_atm are after the turbine
T2_tur = T_atm*(1-eta_comp_lst*(1-(p_atm/p_high)**((kappa_air-1)/kappa_air)))   # [K]
W_sp_tur = cp_air*(T_atm*np.ones(len(T2_tur))-T2_tur)   # [J/kg] Work done *BY* turbine

# ------------------------------ PLOTTING -------------------------------------
fig = plt.figure()
fig.suptitle('Isentropic Efficiencies')

ax1 = fig.add_subplot(2, 2, 1)
ax1.plot(eta_comp_lst*100, T2_comp-273.15, label=r'$T_2$')
ax1.set_title(r'Temperature after compressor at $p_2$ = ' + f'{p_high/1e5:.1f}' + ' bar')
ax1.set_xlabel(r'$\eta_{is, comp}$ [%]')
ax1.set_ylabel(r'$T_2$ [$\degree$C]')
ax1.legend()

ax2 = fig.add_subplot(2, 2, 2)
ax2.plot(eta_comp_lst*100, W_sp_comp/1e3, label=r'$W_{sp, comp}$')
ax2.set_title(r'Specific work on compressor at $p_2$ = ' + f'{p_high/1e5:.1f}' + ' bar')
ax2.set_xlabel(r'$\eta_{is, comp}$ [%]')
ax2.set_ylabel(r'$W_{sp, comp}$ [kJ/kg]')
ax2.legend()

ax3 = fig.add_subplot(2, 2, 3)
ax3.plot(eta_comp_lst*100, T2_tur-273.15, label=r'$T_2$')
ax3.set_title(r'Temperature after turbine at $p_2$ = ' + f'{p_high/1e5:.1f}' + ' bar')
ax3.set_xlabel(r'$\eta_{is, tur}$ [%]')
ax3.set_ylabel(r'$T_2$ [$\degree$C]')
ax3.legend()

ax4 = fig.add_subplot(2, 2, 4)
ax4.plot(eta_comp_lst*100, W_sp_tur/1e3, label=r'$W_{sp, comp}$')
ax4.set_title(r'Specific work by turbine at $p_2$ = ' + f'{p_high/1e5:.1f}' + ' bar')
ax4.set_xlabel(r'$\eta_{is, tur}$ [%]')
ax4.set_ylabel(r'$W_{sp, comp}$ [kJ/kg]')
ax4.legend()

fig.tight_layout()
plt.show()
