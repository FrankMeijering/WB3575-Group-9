import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tools import get_folder_file, eta_comp_func


# ------------------------- VALUES TO ADD MANUALLY ----------------------------
# Enter a time interval over which the mean values should be calculated.
# It is recommended to select a steady-state interval.
# The program will ask you to perform calculations. If the interval is unknown, these should be skipped.
starttime = 70  # in [s]
endtime = 90   # in [s]

# Enter the mass flow percentage read from the meter.
m_dot_percent = 18   # in [%]

# Enter the final pressure achieved (absolute pressure, not pressure difference).
p2 = 2.5  # [bar]

# ----------------------------- DATA DESCRIPTION ------------------------------
# 'time' is the time the test has run in [s]
# 'temp1' is the temperature of the flow, after the compressor
# 'temp2' is the temperature of the outside surface of the compressor
# 'temp3' is the temperature inside the compressor immediately after the test is stopped
# 'temp4' is the atmospheric temperature
# 'torqnm' is the torque input to the compressor in [Nm]
# 'rpm' is the rotational frequency in [revolutions per minute]
# 'torqv', 'rpmv', 'volt', 'curr', 'flow', 'pressure', and 'runtime' are not used here


# ----------------------------- DATA PROCESSING -------------------------------
# Import raw data from Excel file
directory = get_folder_file('data', '21 10 20 11 12 07comp_1.5_28.xls')
total_data = pd.read_csv(directory, sep='\t')   # Pandas dataframe with all Excel data
total_data = total_data.drop(columns=['torqv', 'rpmv', 'volt', 'curr', 'flow', 'pressure', 'runtime'])
headers = list(total_data.columns.values)   # Contains the column titles such as 'time', 'temp1', etc.
t = np.array(total_data[headers[0]])   # Define a dedicated time array for easier plotting
ylabels = [r'Flow Temperature [$\degree$C]', r'Body Temperature [$\degree$C]',
           r'End Temperature in Compressor [$\degree$C]', r'Atmospheric Temperature [$\degree$C]',
           r'Torque [$Nm$]', r'Rotational Frequency [$rpm$]']   # Define y-axes for plotting


# ------------------------------- CALCULATIONS --------------------------------
# Ask if the calculations should be done
loop = True
continue_ = 'n'
while loop:
    continue_ = input('Perform calculations? (y/n): ')
    if continue_ != 'y' and continue_ != 'n':
        loop = True
        print('\nInvalid input. Please enter \'y\' or \'n\'.')
    else:
        loop = False

# Perform calculation if requested
if continue_ == 'y':
    interval = np.logical_and(t > starttime, t < endtime)   # Use to compute mean values

    # Values extracted from the data
    T1 = np.mean(np.array(total_data["temp3"])[interval])+273.15   # [K] Before compressor (atmospheric)
    T2 = np.mean(np.array(total_data["temp1"])[interval])+273.15   # [K] After compressor (in the flow)
    torque = np.mean(np.array(total_data["torqnm"])[interval])   # [Nm]
    rpm = np.mean(np.array(total_data["rpm"])[interval])   # [rpm] Revolutions per minute

    # Other values
    kappa_air = 1.4     # Ratio of specific heats
    R_air = 287.06      # [J/kg.K] Specific gas constant
    cp_air = R_air/(1-1/kappa_air)   # [J/kg.K] Specific heat at constant pressure of air
    V_dot_max = 15.8*1.7    # [m^3/hr] Max measurable volume flow (from datasheet; 1.7 converts from scfm to m3/h).
    p1 = 101325    # [Pa] Before compressor (assumed to be 1 atm)
    p2 *= 10**5    # [Pa] After compressor
    A = np.pi*(0.005**2)   # [m^2] Cross-sectional area of the tube after the compressor

    # Calculations
    rho_air = p1 / (R_air * T2)     # [kg/m^3] Ideal gas law
    m_dot_max = V_dot_max*rho_air/3600    # [kg/s] Maximum measurable mass flow
    m_dot = m_dot_max*m_dot_percent/100   # [kg/s] Actual mass flow
    W_dot = torque*rpm*2*np.pi/60  # [W] Power input by drill
    velocity = m_dot*R_air*T2/(p2*A)  # [m/s] Flow velocity after compressor
    Q_dot = W_dot - m_dot*(cp_air*(T2-T1) - (velocity**2)/2)  # [W] Heat loss
    efficiency = (1 - Q_dot/W_dot)*100  # [%] Compressor efficiency

    print('\n-------------- RESULTS --------------')
    print(f'Power input: {W_dot:.1f} [W]')
    print(f'Heat loss: {Q_dot:.1f} [W]')
    print(f'Efficiency: {efficiency:.3f} [%]')


# ------------------------------ PLOTTING -------------------------------------
fig = plt.figure()
axes = []
i = 0
for header in headers[1:]:
    axes.append(fig.add_subplot(2, 3, i+1))
    axes[-1].plot(t, np.array(total_data[header]))
    axes[-1].set_title(header)
    axes[-1].set_xlabel('Time [s]')
    axes[-1].set_ylabel(ylabels[i])
    i += 1
fig.tight_layout()
plt.show()
