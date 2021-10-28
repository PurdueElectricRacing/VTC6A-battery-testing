import numpy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# overview: plot OCV vs SOC curve for output first mini BMS data

def read_low_current_discharge_and_charge(csv_name):
    reader = pd.read_csv(csv_name, header=10, encoding ='UTF-8')
    df = pd.DataFrame(reader, columns=['Time(S)', 'Cur(A)', 'Vol(V)'])
    data = df.to_numpy()
    data = data.T  ###transpose
    return data


discharge_data = read_low_current_discharge_and_charge(r'../tester-data/10-11/2021-10-12-9-59-48-EBC-A20-1-1-full-discharge.csv')
discharge_data_2 = read_low_current_discharge_and_charge(r'../tester-data/10-17/2021-10-20-21-36-48-EBC-A20-1-1-low-current-full-discharge.csv')
charge_data = read_low_current_discharge_and_charge(r'../tester-data/10-12/2021-10-13-17-2-27-EBC-A20-1-1-full-charge.csv')

fig, ax1 = plt.subplots()

color_red = 'tab:red'
color_green = 'tab:green'
ax1.set_xlabel('time(s)')
ax1.set_ylabel('voltage(V)', color=color_red)
ax1.scatter(discharge_data[0, :], discharge_data[2, :], color=color_red, s=0.5, label="0.15A discharge")
ax1.scatter(charge_data[0, :], charge_data[2, :], color=color_green, s=0.5, label="0.15A charge")
ax1.scatter(discharge_data_2[0, :], discharge_data_2[2, :], color='c', s=0.5, label="0.1A discharge")
ax1.tick_params(axis='y', labelcolor=color_red)
ax1.legend()

ax2 = ax1.twinx()

color_blue = 'tab:blue'
ax2.set_ylabel('current(A)', color=color_blue)
ax2.scatter(discharge_data[0, :], discharge_data[1, :], color=color_blue, s=0.5)
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

SOC_percentage_dis, OCV_begin_to_cutoff_dis = discharge_OCV_vs_SOC_plot_prep(discharge_data)
SOC_percentage_charge, OCV_begin_to_cutoff_charge = charge_OCV_vs_SOC_plot_prep(charge_data)
SOC_percentage_dis_2, OCV_begin_to_cutoff_dis_2 = discharge_OCV_vs_SOC_plot_prep_2(discharge_data_2)


#   plot OCV vs SOC
fig3, ax3 = plt.subplots()
#ax3.plot(SOC_percentage_dis, OCV_begin_to_cutoff_dis, color=color_blue, label="0.15A discharge curve")
#ax3.plot(SOC_percentage_charge, OCV_begin_to_cutoff_charge, color=color_green, label="0.15A charge curve")
#ax3.plot(SOC_percentage_dis_2, OCV_begin_to_cutoff_dis_2, color='c', label="0.10A discharge curve")
ax3.scatter(SOC_percentage_dis, OCV_begin_to_cutoff_dis, s=0.5, color=color_blue, label="0.15A discharge curve")
ax3.scatter(SOC_percentage_charge, OCV_begin_to_cutoff_charge, s=0.5, color=color_green, label="0.15A charge curve")
ax3.scatter(SOC_percentage_dis_2, OCV_begin_to_cutoff_dis_2, s=0.5, color='c', label="0.10A discharge curve")

ax3.xaxis.set_major_formatter(FuncFormatter('{0:.0%}'.format))
ax3.set_title("OCV vs SOC (charge & discharge)")
ax3.set_xlabel('SOC')
ax3.set_ylabel('OCV (V)')
ax3.legend()

#   trying to fit a polynomial to OCV vs SOC
OCV_dis_polynomial = np.poly1d(np.polyfit(SOC_percentage_dis, OCV_begin_to_cutoff_dis, 40))
ax3.plot(SOC_percentage_dis, OCV_dis_polynomial(SOC_percentage_dis), color=color_red)
OCV_charge_polynomial = np.poly1d(np.polyfit(SOC_percentage_charge, OCV_begin_to_cutoff_charge, 40))
ax3.plot(SOC_percentage_charge, OCV_charge_polynomial(SOC_percentage_charge), color=color_red)

plt.show()

# hysteresis testing pre-calc
SOC_target = np.linspace(0,1,num=11)
print(SOC_target)
OCV_dis_target = OCV_dis_polynomial(SOC_target)
OCV_charge_target = OCV_charge_polynomial(SOC_target)

print("OCV_dis_target = ", OCV_dis_target)
print("OCV_charge_target = ", OCV_charge_target)
