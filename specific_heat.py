import numpy as np
import matplotlib.pyplot as plt
from tools import cp_lemmon, kappa_calc


# ---------------------- SET UP FUNCTIONS --------------------------
R = 287.06
dT = 0.1
T = np.arange(293.15, 393.15+dT, dT)   # Range which we measure
cp_lemmon = cp_lemmon(T, R)
kappa_lemmon = kappa_calc(cp_lemmon, R)

# ------------------------ CALCULATIONS ----------------------------
# Calculate the averages
cp_const = np.mean(cp_lemmon)
kappa_const = np.mean(kappa_lemmon)

# Root mean square error between constant approximation and Lemmon
rmse_cp = np.sqrt(((cp_const-cp_lemmon)**2).mean())
rmse_kappa = np.sqrt(((kappa_const-kappa_lemmon)**2).mean())

# Root mean square percent error between Moran and Lemmon
rmspe_cp = 100*np.sqrt(np.mean(((cp_const-cp_lemmon)/cp_lemmon)**2))
rmspe_kappa = 100*np.sqrt(np.mean(((kappa_const-kappa_lemmon)/kappa_lemmon)**2))

print('-------------- RESULTS --------------')
print(f'cp_const: {cp_const:.1f} [J/kgK]')
print(f'kappa_const: {kappa_const:.4f} [-]')
print(f'RMSE cp: {rmse_cp:.3f} [J/kgK]')
print(f'RMSPE cp: {rmspe_cp:.3f} [%]')
print(f'RMSE kappa: {rmse_kappa:.5f} [-]')
print(f'RMSPE kappa: {rmspe_kappa:.4f} [%]')

# ------------------------- PLOTTING -------------------------------
# Plot for cp
fig1 = plt.figure()
ax1 = fig1.add_subplot(1, 1, 1)
ax1.set_title('Specific Heat vs Temperature')
ax1.set_xlabel(r'Temperature $T$ [$\degree$C]')
ax1.set_ylabel(r'Specific Heat Capacity $c_p$ [J/kg$\cdot$K]')
ax1.plot(T-273.15, cp_lemmon, label='Lemmon model')
ax1.plot(T-273.15, cp_const*np.ones(len(T)), label='Constant approx.')
ax1.legend()

# Plot for kappa
fig2 = plt.figure()
ax2 = fig2.add_subplot(1, 1, 1)
ax2.set_title('Specific Heat Ratio vs Temperature')
ax2.set_xlabel(r'Temperature $T$ [$\degree$C]')
ax2.set_ylabel(r'Ratio of Specific Heats $\kappa=c_p/c_v$ [-]')
ax2.plot(T-273.15, kappa_lemmon, label='Lemmon model')
ax2.plot(T-273.15, kappa_const*np.ones(len(T)), label='Constant approx.')
ax2.legend()

plt.show()
