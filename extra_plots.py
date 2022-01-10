import numpy as np
from tools import import_file, kappa_air, p_atm
import matplotlib.pyplot as plt

# ----------------------- TEMPERATURES STAIRCASE PRESSURE TEST ----------------------------
filename1 = '21 12 06 11 29 43comp_versnelling1_drukverschil.xls'

# Import raw data from Excel file
total_data, headers, t, ylabels = import_file(filename1)

# Make figure
fig1 = plt.figure()
ax1 = fig1.add_subplot(1, 1, 1)

interval1 = np.logical_and(t > 25, t < 500)  # Use to compute mean values
interval2 = np.logical_and(t > 3310, t < 3820)

ax1.plot(t[interval1]-t[interval1][0], total_data['temp1'][interval1], label='Temperature During Pressure Increase')
ax1.plot(t[interval2]-t[interval2][0], total_data['temp1'][interval2], label='Temperature During Pressure Decrease')
ax1.axhline(35, color='black', linestyle='dotted', label='Expected Steady-State Temperature')

ax1.set_xlabel('Time [s]')
ax1.set_ylabel(r'Flow Temperature at 1.5 bar [$\degree$C]')
ax1.legend()

# ----------------------------- TEMPERATURE VS PRESSURE COMPRESSOR ----------------------------
# Experimental values
dp = 0.5
p = np.arange(1.5, 4.0+dp, dp)
T_nocooling = np.array([[35, 43, 48, 51, 53, 55]])
T_cooling = np.array([[np.nan, np.nan, 26.01, np.nan, np.nan, np.nan]])

# Adiabatic values
T_adiabatic = (19.5+273.15)*(p*1e5/p_atm)**((kappa_air-1)/kappa_air)-273.15

# Isothermal values
T_isothermal = np.array([[19.5]*len(p)])

# Plot
fig2 = plt.figure()
ax2 = fig2.add_subplot(1, 1, 1)
ax2.scatter(p, T_isothermal, color='C2', label='Isothermal')
ax2.scatter(p, T_adiabatic, color='C0', label='Adiabatic')
ax2.scatter(p, T_nocooling, color='C1', label='Experimental (no cooling)')
ax2.scatter(p, T_cooling, color='C3', label='Experimental (cooling)')
ax2.legend()

ax2.set_xlabel('Pressure After Compressor [bar]')
ax2.set_ylabel(r'Temperature After Compressor [$\degree$C]')

# ----------------------------- TEMPERATURE VS PRESSURE TURBINE ----------------------------
# Experimental values
p = np.array([[1.5, 2.0, 2.5, 3.0, 3.5, 4.0]])
T_turb = np.array([[19.5, 10.80, 6.50, 3.10, -1.50, -5.43]])

# Adiabatic values
T_adiabatic = (19.5+273.15)*(p_atm/(p*1e5))**((kappa_air-1)/kappa_air)-273.15

# Isothermal values
T_isothermal = np.array([[19.5]*len(p[0])])

# Plot
fig3 = plt.figure()
ax3 = fig3.add_subplot(1, 1, 1)
ax3.scatter(p, T_isothermal, label='Isothermal', color='C2', zorder=1)
ax3.scatter(p, T_adiabatic, label='Adiabatic', color='C0', zorder=2)
ax3.scatter(p, T_turb, label='Experimental', color='C1', zorder=3)
ax3.legend()

ax3.set_xlabel('Pressure Before Turbine [bar]')
ax3.set_ylabel(r'Temperature After Turbine [$\degree$C]')

plt.show()
