import numpy as np
from tools import eta_tur_func, import_file, ask_question, multiple_plots, extra_file_info, \
    R_air, cp_air, kappa_air, p_atm, V_dot_max, A

# # ----------------------------- IMPORT DATA ----------------------------------
# Enter the name of the file within the 'data' folder
filename = '21 11 29 11 04 30tur_1.5bar.xls'
filename = '21 11 18 11 59 11tur_multimeter10ohm_anderhalf_bar.xls'
# Import raw data from Excel file
total_data, headers, t, ylabels = import_file(filename)

# ------------------------------- CALCULATIONS --------------------------------
# Ask if the calculations should be done
continue_ = ask_question('Data available in \'extra_file_info.xls\'? (y/n): ')

# Perform calculation if requested
if continue_ == 'y':
    ans = ask_question('Do you want to plot lines for start- and endtimes? (y/n): ')
    if ans == 'y':
        plotlines = True
    else:
        plotlines = False

    extra_info, ylabels = extra_file_info(filename)
    interval = np.logical_and(t > extra_info[0], t < extra_info[1])   # Use to compute mean values

    # Values extracted from data
    T1 = np.mean(np.array(total_data[extra_info[4]])[interval])+273.15   # [K] Before compressor (atmospheric)
    T2 = np.mean(np.array(total_data[extra_info[5]])[interval])+273.15   # [K] After compressor (in the flow)
    torque = np.mean(np.array(total_data["torqnm"])[interval])   # [Nm]
    rpm = np.mean(np.array(total_data["rpm"])[interval])   # [rpm] Revolutions per minute
    p1 = 1e5*extra_info[3]    # [Pa] Before compressor (assumed to be 1 atm)
    p2 = p_atm    # [Pa] After compressor
    m_dot_percent = extra_info[2]

    # Calculations
    rho_air_1 = p1 / (R_air * T1)     # [kg/m^3] Ideal gas law for station 1, to calculate velocity1 and the mass flow
    rho_air_2 = p2 / (R_air * T2)     # [kg/m^3] Ideal gas law for station 2, to calculate velocity2
    m_dot_max = V_dot_max*rho_air_1    # [kg/s] Maximum measurable mass flow (uses rho1 since the flowmeter is there)
    m_dot = m_dot_max*m_dot_percent/100   # [kg/s] Actual mass flow
    W_dot = torque*rpm*2*np.pi/60  # [W] Power output from turbine into drill (positive)
    velocity1 = m_dot/(rho_air_1*A)  # [m/s] Flow velocity before turbine
    velocity2 = m_dot/(rho_air_2*A)  # [m/s] Flow velocity after turbine
    Q_dot = W_dot-m_dot*(cp_air*(T1-T2)+(velocity1**2)/2-(velocity2**2)/2)  # [W] Heat input (positive)
    efficiency_tur_is = eta_tur_func(T1, T2, p1, p2, kappa_air)*100  # [%] Isentropic efficiency (valid if Q_dot=0)

    print('\n-------------- RESULTS --------------')
    print(f'Power: {W_dot:.1f} [W]')
    print(f'Heat: {Q_dot:.1f} [W]')
    print(f'Temperature change: {T2-T1:.2f} deg Celsius')
    print(f'Enthalpy change: {m_dot*cp_air*(T2-T1):.2f} [W]')
    print(f'Kinetic energy change: {m_dot*((velocity2**2)/2-(velocity1**2)/2):.2f} [W]')
    print(f'Volume flow: {V_dot_max*m_dot_percent*10:.2f} [L/s]')
    print(f'Mass flow: {m_dot:.5f} [kg/s]')
    print(f'Isentropic turbine efficiency: {efficiency_tur_is:.3f} [%]')
    print('-------------------------------------')

    # ------------------------------ PLOTTING -------------------------------------
    multiple_plots(filename, headers, total_data, ylabels, t, extra_info, plotlines)
else:
    multiple_plots(filename, headers, total_data, ylabels, t, 0, False)
