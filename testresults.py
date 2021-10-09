import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tools import get_folder_file

directory = get_folder_file('data', '21 10 05 12 54 26.txt')
total_data = pd.read_csv(directory, sep='\t')
headers = list(total_data.columns.values)
t = total_data[headers[0]]

# ------------------------------ PLOTTING -------------------------------------
fig = plt.figure()
axes = []
i = 0
for header in headers[1:]:
    axes.append(fig.add_subplot(3, 3, i+1))
    axes[i].plot(t, total_data[header])
    axes[i].set_title(header)
    i += 1
plt.show()
