import numpy as np
from tools import eta_comp_func, import_file, ask_question, multiple_plots, \
    R_air, cp_air, kappa_air, p_atm, V_dot_max, A

# ------------------------- VALUES TO ADD MANUALLY ----------------------------
# Enter the name of the file within the 'data' folder
filename = '21 11 15 11 03 52halfhourwarmup_cmp_1.5bar.xls'

# Enter a time interval over which the mean values should be calculated.
# It is recommended to select a steady-state interval.
# The program will ask you to perform calculations. If the interval is unknown, these should be skipped.
starttime = 950  # in [s]
endtime = 1000   # in [s]

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
# The remaining values are not used here

# ----------------------------- DATA PROCESSING -------------------------------
# Import raw data from Excel file
total_data, headers, t, ylabels = import_file(filename)

# ------------------------------- CALCULATIONS --------------------------------
# Ask if the calculations should be done
continue_ = ask_question()

# Perform calculation if requested
if continue_ == 'y':
    interval = np.logical_and(t > starttime, t < endtime)   # Use to compute mean values

    # Values extracted from data
    T1 = np.mean(np.array(total_data["temp4"])[interval])+273.15   # [K] Before compressor (atmospheric)
    T2 = np.mean(np.array(total_data["temp1"])[interval])+273.15   # [K] After compressor (in the flow)
    torque = np.mean(np.array(total_data["torqnm"])[interval])   # [Nm]
    rpm = np.mean(np.array(total_data["rpm"])[interval])   # [rpm] Revolutions per minute
    p1 = p_atm    # [Pa] Before compressor (assumed to be 1 atm)
    p2 *= 10**5    # [Pa] After compressor

    # Calculations
    rho_air_1 = p1 / (R_air * T1)   # [kg/m^3] Ideal gas law for station 1, to calculate the mass flow and velocity1
    rho_air_2 = p2 / (R_air * T2)   # [kg/m^3] Ideal gas law for station 2, to calculate the mass flow and velocity2
    m_dot_max = V_dot_max*rho_air_2    # [kg/s] Maximum measurable mass flow (uses rho2 since the flowmeter is there)
    m_dot = m_dot_max*m_dot_percent/100   # [kg/s] Actual mass flow
    W_dot = -torque*rpm*2*np.pi/60  # [W] Power input by drill (negative)
    velocity1 = m_dot/(rho_air_1*A)  # [m/s] Flow velocity before compressor
    velocity2 = m_dot/(rho_air_2*A)  # [m/s] Flow velocity after compressor
    Q_dot = W_dot-m_dot*(cp_air*(T1-T2)+(velocity1**2)/2-(velocity2**2)/2)  # [W] Heat input (negative)
    efficiency_comp_is = eta_comp_func(T1, T2, p1, p2, kappa_air)*100  # [%] Isentropic efficiency (valid if Q_dot=0)

    print('\n-------------- RESULTS --------------')
    print(f'Power: {W_dot:.1f} [W]')
    print(f'Heat: {Q_dot:.1f} [W]')
    print(f'Temperature change: {T2-T1:.2f} deg Celsius')
    print(f'Enthalpy change: {m_dot*cp_air*(T2-T1):.2f} [W]')
    print(f'Kinetic energy change: {m_dot*((velocity2**2)/2-(velocity1**2)/2):.2f} [W]')
    print(f'Volume flow: {V_dot_max*m_dot_percent*10:.2f} [L/s]')
    print(f'Mass flow: {m_dot:.5f} [kg/s]')
    print(f'Isentropic compressor efficiency: {efficiency_comp_is:.3f} [%]')
    print('-------------------------------------')

# ------------------------------ PLOTTING -------------------------------------
multiple_plots(filename, headers, total_data, ylabels, t)
