import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# --------------------------- FUNCTIONS -------------------------------
def get_file(file):
    # Returns the full path, if the file is in the same folder as the main .py program.
    return os.path.join(os.path.dirname(file), file)


def get_folder_file(folder, file):
    # Returns the full path, if the file is not in the same folder as the main .py program.
    # If this does not work, use: return get_file(os.path.join(folder, file))
    return os.path.join(folder, file)


def eta_comp_func(T1, T2, p1, p2, kappa):
    return ((p2/p1)**((kappa-1)/kappa)-1)/(T2/T1-1)


def eta_tur_func(T1, T2, p1, p2, kappa):
    return (T2/T1-1)/((p2/p1)**((kappa-1)/kappa)-1)


def cp_lemmon(T, R):
    # Specific heat cp according to Lemmon
    return R*(3.491+2.396e-6*T+7.172e-9*T**2-3.115e-13*T**3+0.224*T**-1.5+0.791*((3364/T)**2)*np.exp(3364/T)/
              ((np.exp(3364/T)-1)**2)+0.212*((2242/T)**2)*np.exp(2242/T)/((np.exp(2242/T)-1)**2)+
              (2/3)*0.198*((11580/T)**2)*np.exp(-11580/T)/(((2/3)*np.exp(-11580/T)+1)**2))


def kappa_calc(cp, R):
    return 1/(1-R/cp)


def import_file(filename):
    # Make sure the header row is added to the Excel file, and that the commas are changed to points.
    directory = get_folder_file('data', filename)
    total_data = pd.read_csv(directory, sep='\t')  # Pandas dataframe with all Excel data
    total_data = total_data.drop(columns=['torqv', 'rpmv', 'volt', 'curr', 'flow', 'pressure', 'runtime'])
    headers = list(total_data.columns.values)  # Contains the column titles such as 'time', 'temp1', etc.
    t = np.array(total_data[headers[0]])  # Define a dedicated time array for easier plotting
    ylabels = [r'Temperature 1 [$\degree$C]', r'Temperature 2 [$\degree$C]',
               r'Temperature 3 [$\degree$C]', r'Temperature 3 [$\degree$C]',
               r'Torque [$Nm$]', r'Rotational Frequency [$rpm$]']  # y-axes in case the extra info is unavailable.
    return total_data, headers, t, ylabels


def ask_question():
    # Ask the user if they want to perform calculations or not.
    loop = True
    continue_ = 'n'
    while loop:
        continue_ = input('Perform calculations? (y/n): ')
        if continue_ != 'y' and continue_ != 'n':
            loop = True
            print('\nInvalid input. Please enter \'y\' or \'n\'.')
        else:
            loop = False
    return continue_


def multiple_plots(filename, headers, total_data, ylabels, t):
    # Plot all relevant data in a single figure.
    fig = plt.figure()
    fig.suptitle('File:   ' + filename)
    axes = []
    i = 0
    for header in headers[1:]:   # One header corresponds to one axis system
        axes.append(fig.add_subplot(2, 3, i + 1))
        axes[-1].plot(t, np.array(total_data[header]))
        axes[-1].set_title(header)
        axes[-1].set_xlabel('Time [s]')
        axes[-1].set_ylabel(ylabels[i])
        i += 1
    fig.tight_layout()
    plt.show()


def combined_plots(filenames, headers, total_data_lst, ylabels_lst, t):
    # Plots of multiple tests in one figure

    # First make sure the plots in one figure represent the same quantities.
    # Take the first test as reference.
    i = 1  # start at the second test
    for ylabels in ylabels_lst[1:]:  # Look at all tests except the first one
        for k in range(len(ylabels_lst[0])):  # Look through the labels of the first test
            if ylabels_lst[0][k] != ylabels[k]:  # If the labels do not match
                for n in range(len(ylabels)):  # Look through the labels of the current test
                    if ylabels_lst[0][k] == ylabels[n]:  # Look for which they do match, swap the current test values
                        ylabels[k], ylabels[n] = ylabels[n], ylabels[k]

                        # index +1 since the 'time' column is not used
                        headers_temporary = list(headers)  # Use 'list' to make the headers immutable
                        headers_temporary[k+1], headers_temporary[n+1] = headers_temporary[n+1], headers_temporary[k+1]
                        total_data_lst[i] = total_data_lst[i].reindex(columns=headers_temporary)
                        total_data_lst[i].columns = headers
        i += 1

    fig = plt.figure()
    fig.suptitle('Results of Multiple Tests')
    axes = []
    i = 0
    for header in headers[1:]:  # One header corresponds to one axis system
        axes.append(fig.add_subplot(2, 3, i + 1))
        x = 0
        for data in total_data_lst:  # Plot the info from the multiple tests, all in the same axis system
            if i == 0:  # colours remain the same, so only need one legend
                axes[-1].plot(t, np.array(data[header]),
                              label=filenames[x][17:])  # cut part of the filename out
            else:
                axes[-1].plot(t, np.array(data[header]))
            x += 1
        axes[-1].set_title(header)
        axes[-1].set_xlabel('Time [s]')
        axes[-1].set_ylabel(ylabels_lst[0][i])
        i += 1
    fig.legend(bbox_to_anchor=(1, 1))
    fig.tight_layout()
    plt.show()


def extra_file_info(filename, comptrue):
    # comptrue is True if it is the compressor test, and False if it the turbine test.
    # If 'n.a.' is given, it means this value is irrelevant.
    directory = get_folder_file('data', 'extra_file_info.xls')
    total_file = pd.read_csv(directory, sep='\t')  # Pandas dataframe with all Excel data
    row = np.array(total_file.loc[total_file['filename'] == filename])[0][1:]  # Remove first column
    # Values in row are: [starttime, endtime, mflow_percent, pressure_abs,
    # temp_before, temp_after, temp_body, temp_atm, temp_water, temp_unused]

    # Update ylabels from import_file from the extra information
    ylabels = ['temp1', 'temp2', 'temp3', 'temp4', r'Torque [$Nm$]', r'Rotational Frequency [$rpm$]']

    word = 'Turbine'
    if comptrue:
        word = 'Compressor'

    temps = ['Temperature Before ' + word + r' [$\degree$C]',
             'Temperature After ' + word + r' [$\degree$C]',
             r'Body Temperature [$\degree$C]',
             r'Atmospheric Temperature [$\degree$C]',
             'Water Temperature After ' + word + r' [$\degree$C]',
             r'Unused Temperature [$\degree$C]']

    row_temps = row[4:]  # Extract the temperature data
    for j in range(4):  # 4 temperature locations in ylabels
        for i in range(len(row_temps)):  # quantities from the extra data file
            if row_temps[i] == ylabels[j]:
                ylabels[j] = temps[i]

    return row, ylabels


# --------------------------- CONSTANTS ---------------------------
R_air = 287.06      # [J/kg.K] Specific gas constant
cp_air = 1007.9  # [J/kg.K] Found with specific_heat.py
kappa_air = 1.3982  # Found with specific_heat.py
p_atm = 101325  # [Pa] Before compressor (assumed to be 1 atm)
V_dot_max = 0.0045  # [m^3/s]  Determined with calibration
A = np.pi * (0.004 ** 2)  # [m^2] Cross-sectional area of the compressor/turbine inlet and outlet
T1w = 15 + 273.15  # [K] Temperature of the tap water
