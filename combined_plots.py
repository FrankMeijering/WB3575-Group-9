from tools import import_file, extra_file_info, combined_plots
import numpy as np
import pandas as pd

# # ----------------------------- IMPORT DATA ----------------------------------
# Enter the name of the file within the 'data' folder
filenames = ['21 11 29 15 07 47comp_1.5bar_cooling_high_mflow.xls',
             '21 11 29 15 39 41comp_1.5bar_cooling_low_mflow.xls',
             '21 11 29 17 00 18comp_1.5bar_cooling_medium_mflow.xls']

total_data_lst = []
t_lst = []
extra_info_lst = []
ylabels_lst = []

for file in filenames:
    # Import raw data from Excel file
    total_data, headers, t, _ = import_file(file)
    extra_info, ylabels = extra_file_info(file, False)
    total_data_lst.append(total_data)
    t_lst.append(t)
    extra_info_lst.append(extra_info)
    ylabels_lst.append(ylabels)

# Scale axes to the test with the longest time axis
lengths = []
for t_temporary in t_lst:
    lengths.append(len(t_temporary))
longest_t = t_lst[np.argmax(lengths)]
shortest_t = t_lst[np.argmin(lengths)]

for i in range(len(filenames)):   # Add zeroes
    if len(t_lst[i]) != len(longest_t):
        zero_matrix = np.zeros((len(longest_t) - len(t_lst[i]), len(headers)))
        zero_matrix.fill(np.nan)  # Replace zeroes by 'NaN' to prevent plotting zeroes in the figures
        zero_dataframe = pd.DataFrame(zero_matrix)
        zero_dataframe.columns = headers
        total_data_lst[i] = total_data_lst[i].append(zero_dataframe)

# ------------------------------ PLOTTING -------------------------------------
combined_plots(filenames, headers, total_data_lst, ylabels_lst, longest_t)
