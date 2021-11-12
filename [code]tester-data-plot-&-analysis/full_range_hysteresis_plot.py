import numpy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# overview: plot OCV vs SOC curve for output first mini BMS data
# TODO: divid the full capacity time and place each charge/discharge cycle
#  in the correct location of the SOC plot

def read_low_current_discharge_and_charge(csv_name):
    reader = pd.read_csv(csv_name, header=10, encoding ='UTF-8')
    df = pd.DataFrame(reader, columns=['Time(S)', 'Cur(A)', 'Vol(V)'])
    data = df.to_numpy()
    data = data.T  ###transpose
    return data

# assume charge time in 0.15A from 0% to 100% SOC (based on previous testing)
full_charge_time = 93804 # (s)
full_discharge_time = 107744 # (s)

total_data = read_low_current_discharge_and_charge(r'../tester-data/10-22/2021-10-27-19-38-32-EBC-A20-1-1_hysteresis.csv')

time_sheet = np.array([[95442, 172278], [177352, 254022], [254022, 314828], [316626, 373273], [373273, 412682], [412754, 445245],
                       [445245, 469996], [479665, 490782], [490782, 498115]])

current_index_start = np.where(total_data[0, :] == time_sheet[0][0])[0][0]
current_index_end = np.where(total_data[0, :] == time_sheet[0][1])[0][0]
charge_data_0_to_90 = total_data[:, current_index_start:current_index_end]
current_time_data = total_data[0, current_index_start:current_index_end]
print(current_time_data)
print(current_time_data[0])
SOC_0_to_90 = 0.9 * ((current_time_data - current_time_data[0])/(total_data[0, current_index_end] - total_data[0, current_index_start]))
#SOC_0_to_90 = 0.9 * ((current_time_data)/(total_data[0, current_index_end] - total_data[0, current_index_start]))
#SOC_0_to_90 = 0.9 * np.arange(172278 - 95442)/(172278 - 95442)

current_index_start = np.where(total_data[0, :] == time_sheet[1][0])[0][0]
current_index_end = np.where(total_data[0, :] == time_sheet[1][1])[0][0]
discharge_data_90_to_10 = total_data[:, current_index_start:current_index_end]
current_time_data = total_data[0, current_index_start:current_index_end]
print(current_time_data)
print(current_time_data[0])
SOC_90_to_10 = 0.9 - 0.8 * ((current_time_data - current_time_data[0])/(total_data[0, current_index_end] - total_data[0, current_index_start]))

current_index_start = np.where(total_data[0, :] == time_sheet[2][0])[0][0]
current_index_end = np.where(total_data[0, :] == time_sheet[2][1])[0][0]
charge_data_10_to_80 = total_data[:, current_index_start:current_index_end]
current_time_data = total_data[0, current_index_start:current_index_end]
print(current_time_data)
print(current_time_data[0])
SOC_10_to_80 = 0.1 + 0.7 * ((current_time_data - current_time_data[0])/(total_data[0, current_index_end] - total_data[0, current_index_start]))

current_index_start = np.where(total_data[0, :] == time_sheet[3][0])[0][0]
current_index_end = np.where(total_data[0, :] == time_sheet[3][1])[0][0]
discharge_data_80_to_20 = total_data[:, current_index_start:current_index_end]
current_time_data = total_data[0, current_index_start:current_index_end]
print(current_time_data)
print(current_time_data[0])
SOC_80_to_20 = 0.8 - 0.6 * ((current_time_data - current_time_data[0])/(total_data[0, current_index_end] - total_data[0, current_index_start]))

charge_data_20_to_70 = total_data[:, (np.where(total_data[0, :] == 373273)[0][0]):(np.where(total_data[0, :] == 412682)[0][0])]
discharge_data_70_to_30 = total_data[:, (np.where(total_data[0, :] == 412754)[0][0]):(np.where(total_data[0, :] == 445245)[0][0])]
charge_data_30_to_60 = total_data[:, (np.where(total_data[0, :] == 445245)[0][0]):(np.where(total_data[0, :] == 469996)[0][0])]
discharge_data_60_to_40 = total_data[:, (np.where(total_data[0, :] == 470665)[0][0]):(np.where(total_data[0, :] == 490782)[0][0])]
charge_data_40_to_50 = total_data[:, (np.where(total_data[0, :] == 490782)[0][0]):(np.where(total_data[0, :] == 498115)[0][0])]


fig, ax1 = plt.subplots()

test_plot = charge_data_40_to_50

color_red = 'tab:red'
color_green = 'tab:green'
ax1.set_xlabel('time(s)')
ax1.set_ylabel('voltage(V)', color=color_red)
ax1.scatter(test_plot[0, :], test_plot[2, :], color=color_red, s=0.5, label="0.15A")
ax1.tick_params(axis='y', labelcolor=color_red)
ax1.legend()

ax2 = ax1.twinx()

color_blue = 'tab:blue'
ax2.set_ylabel('current(A)', color=color_blue)
ax2.scatter(test_plot[0, :], test_plot[1, :], color=color_blue, s=0.5)
ax2.tick_params(axis='y', labelcolor=color_blue)

fig.tight_layout()
plt.show()

# --- generate OCV vs SOC plot ---

def discharge_OCV_vs_SOC_plot_prep(data):

    SOC_begin_index = np.where(data[2, :] <= 2.45)[0][0]
    SOC_begin_time = data[0, SOC_begin_index]
    SOC_cutoff_index = np.where(data[2, :] >= 4.224)[0][0]
    SOC_cutoff_time = data[0, SOC_cutoff_index]
    SOC_percentage = 1 - data[0, SOC_cutoff_index:SOC_begin_index] / (SOC_begin_time - SOC_cutoff_time)
    OCV_begin_to_cutoff = data[2, SOC_cutoff_index:SOC_begin_index]

    return SOC_percentage, OCV_begin_to_cutoff

def discharge_OCV_vs_SOC_plot_prep_2(data):

    SOC_begin_index = np.where(data[2, :] <= 2.4)[0][0]
    SOC_begin_time = data[0, SOC_begin_index]
    SOC_cutoff_index = np.where(data[2, :] >= 4.173)[0][0]
    SOC_cutoff_time = data[0, SOC_cutoff_index]
    SOC_percentage = 1 - data[0, SOC_cutoff_index:SOC_begin_index] / (SOC_begin_time - SOC_cutoff_time)
    OCV_begin_to_cutoff = data[2, SOC_cutoff_index:SOC_begin_index]

    return SOC_percentage, OCV_begin_to_cutoff

def charge_OCV_vs_SOC_plot_prep(data):

    SOC_begin_index = np.where(data[2, :] <= 2.455)[0][0]
    SOC_begin_time = data[0, SOC_begin_index]
    SOC_cutoff_index = np.where(data[2, :] >= 4.2)[0][0]
    SOC_cutoff_time = data[0, SOC_cutoff_index]
    SOC_percentage = data[0, SOC_begin_index:SOC_cutoff_index] / (SOC_cutoff_time - SOC_begin_time)
    OCV_begin_to_cutoff = data[2, SOC_begin_index:SOC_cutoff_index]

    return SOC_percentage, OCV_begin_to_cutoff



#   plot OCV vs SOC
fig3, ax3 = plt.subplots()
#ax3.plot(SOC_percentage_dis, OCV_begin_to_cutoff_dis, color=color_blue, label="0.15A discharge curve")
#ax3.plot(SOC_percentage_charge, OCV_begin_to_cutoff_charge, color=color_green, label="0.15A charge curve")
#ax3.plot(SOC_percentage_dis_2, OCV_begin_to_cutoff_dis_2, color='c', label="0.10A discharge curve")
print(len(charge_data_0_to_90[2,:]))
print(len(SOC_0_to_90))
ax3.scatter(SOC_0_to_90, charge_data_0_to_90[2,:], s=0.5, color='b', label="0% to 90% charge")
ax3.scatter(SOC_90_to_10, discharge_data_90_to_10[2,:], s=0.5, color='r', label="90% to 10% discharge")
ax3.scatter(SOC_10_to_80, charge_data_10_to_80[2,:], s=0.5, color='c', label="10% to 80% charge")
ax3.scatter(SOC_80_to_20, discharge_data_80_to_20[2,:], s=0.5, color='g', label="80% to 20% discharge")

ax3.xaxis.set_major_formatter(FuncFormatter('{0:.0%}'.format))
ax3.set_title("OCV vs SOC (charge & discharge)")
ax3.set_xlabel('SOC')
ax3.set_ylabel('OCV (V)')
ax3.legend()
plt.show()


