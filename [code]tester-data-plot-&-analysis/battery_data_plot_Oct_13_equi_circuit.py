import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# overview: plot OCV vs SOC curve for output first mini BMS data


# reader = pd.read_csv(r'10-13/equiv-circuit-1st-part-2021-10-14-8-33-31-EBC-A20-1-1.csv', header=22, encoding = 'UTF-8')
reader = pd.read_csv(r'../tester-data/10-15/2021-10-15-17-42-11-EBC-A20-1-1-lower-voltage-equi-circuit.csv', header=14, encoding ='UTF-8')
print(reader)
df = pd.DataFrame(reader, columns=['Time(S)', 'Cur(A)', 'Vol(V)'])
print(df)
data = df.to_numpy()

#top = np.where(data[:, 0] > 100000)[0][0]
#bottom = np.where(data[:, 0] > 40000)[0][0]  ### finding the needed points
#bottom = np.where(data[:, 0] > 0)[0][0]  ### finding the needed points

#data = data[bottom:top, :]  ### slicing the requireed dataset

data = data.T  ###transpose
print(data)

swpts = []

for i in range(len(data[0]) - 1):  # finding the swich points
    if abs(data[2, i + 1] - data[2, i]) > 100:
        swpts.append(i)

print(len(swpts))

fig, ax1 = plt.subplots()

color_red = 'tab:red'
ax1.set_xlabel('time(s)')
ax1.set_ylabel('voltage(V)', color=color_red)
ax1.scatter(data[0, :], data[2, :], color=color_red, s=0.5)
ax1.tick_params(axis='y', labelcolor=color_red)

ax2 = ax1.twinx()

color_blue = 'tab:blue'
ax2.set_ylabel('current(A)', color=color_blue)
ax2.scatter(data[0, :], data[1, :], color=color_blue, s=0.5)
ax2.tick_params(axis='y', labelcolor=color_blue)

fig.tight_layout()
plt.show()

# --- generate OCV vs SOC plot ---

# calculate OCV
#   begin voltage = 2.550 V, cutoff voltage = 4.200 V
SOC_begin_index = np.where(data[2, :] <= 2.55)[0][0]
SOC_begin_time = data[0, SOC_begin_index]
SOC_cutoff_index = np.where(data[2, :] >= 4.2)[0][0]
SOC_cutoff_time = data[0, SOC_cutoff_index]

SOC_percentage = data[0, SOC_begin_index:SOC_cutoff_index] / (SOC_cutoff_time - SOC_begin_time)
OCV_begin_to_cutoff = data[2, SOC_begin_index:SOC_cutoff_index]

#   plot OCV vs SOC
fig3, ax3 = plt.subplots()
ax3.plot(SOC_percentage, OCV_begin_to_cutoff, color=color_blue)
ax3.xaxis.set_major_formatter(FuncFormatter('{0:.0%}'.format))
ax3.set_title("OCV vs SOC (charging)")
ax3.set_xlabel('SOC')
ax3.set_ylabel('OCV (V)')

#   trying to fit a polynomial to OCV vs SOC
OCV_polynomial = np.poly1d(np.polyfit(SOC_percentage, OCV_begin_to_cutoff, 20))
ax3.plot(SOC_percentage, OCV_polynomial(SOC_percentage), color=color_red)

plt.show()


