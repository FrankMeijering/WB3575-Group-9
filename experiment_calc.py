import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tools import get_folder_file, eta_comp_func

# ----------------------------- DATA PROCESSING -------------------------------
directory = get_folder_file('data', '21 10 12 12 23 05leeglopen_rt_10.xls')
total_data = pd.read_csv(directory, sep='\t')
headers = list(total_data.columns.values)
t = np.array(total_data[headers[0]])

interval1 = np.logical_and(t > 15, t < 23)  # Use this to select intervals in any array
interval2 = np.logical_and(t > 8, t < 10)
interval3 = np.logical_and(t > 2.5, t < 5)

T1 = np.mean(np.array(total_data["temp1"])[interval1])+273.15   # [K]
T2 = 440
p1 = 101325    # Analog measurement   [Pa]
p2 = 300000    # Analog measurement
m_dot_analog = 1e-3   # Analog measurement   [kg/s]
#torq = np.mean(np.array(total_data["torqnm"])[interval2])   # [Nm]
#rpm = np.mean(np.array(total_data["rpm"])[interval3])   # [rpm]

# ------------------------------ CONSTANTS ------------------------------------
kappa_air = 1.4     # Ratio of specific heats
R_uni = 8.31446     # Universal gas constant in J/mol.K
R_air = 287.06      # Specific gas constant in J/kg.K
cp_air = R_air/(1-1/kappa_air)   # Specific heat at constant pressure of air in J/kg.K

# ----------------------------- CALCULATIONS ----------------------------------
eta_comp = eta_comp_func(T1, T2, p1, p2, kappa_air)
#power = torq*rpm*2*np.pi/60
# m_dot_calc = power / (cp_air*(T2-T1))    # Not sure about this one

# ------------------------------ PLOTTING -------------------------------------
fig = plt.figure()
axes = []
i = 0
for header in headers[1:]:
    axes.append(fig.add_subplot(4, 4, i+1))
    axes[i].plot(t, np.array(total_data[header]))
    axes[i].set_title(header)
    i += 1
fig.tight_layout()
plt.show()
