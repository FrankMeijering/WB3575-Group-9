from tools import import_file, multiple_plots
# # ----------------------------- IMPORT DATA ----------------------------------
# Enter the name of the file within the 'data' folder
filename = '21 11 29 15 07 47comp_1.5bar_cooling_high_mflow.xls'

# Import raw data from Excel file
total_data, headers, t, ylabels = import_file(filename)

# ------------------------------ PLOTTING -------------------------------------
multiple_plots(filename, headers, total_data, ylabels, t)

# TODO: not working yet.
# TODO: combine multiple files in a single plot. Use the extra file data from the Excel sheet.
