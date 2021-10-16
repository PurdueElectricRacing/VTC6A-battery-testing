import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error

### overview: manually set range of exponential curve to get RC constant

reader = pd.read_csv(r'../tester-data/10-13/equiv-circuit-1st-part-2021-10-14-8-33-31-EBC-A20-1-1.csv', header=22, encoding ='UTF-8')
print(reader)
df = pd.DataFrame(reader, columns=['Time(S)', 'Cur(A)', 'Vol(V)'])
print(df)
data = df.to_numpy()

delta_i = 2 # (A)

top = np.where(data[:, 0] > 7494)[0][0] # original crop: 48400
#bottom = np.where(data[:, 0] > 40000)[0][0]  ### finding the needed points
bottom = np.where(data[:, 0] > 6847)[0][0]  ### finding the needed points, original = 44884
v_top = data[top, 2]



data = data[bottom:top, :]  ### slicing the requireed dataset
data = data.T  ###transpose

print(data)
# swpts = []
#
# for i in range(len(data[0]) - 1):  # finding the swich points
#     if abs(data[2, i + 1] - data[2, i]) > 100:
#         swpts.append(i)
#
# print(len(swpts))

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

# rising edge detection

i = 1
while(data[2,i] >= data[2, i+1] - 0.005):
    #print(data[1, i])
    i = i+1
#print(i)
delta_v_0 = data[2, i+1] - data[2, i]
print("delta_v_0 = ", delta_v_0*1000, "(mV)")
R_0 = delta_v_0 / delta_i
delta_v_inf = v_top - data[2, i]
print("delta_v_inf = ", delta_v_inf*1000, "(mV)")
R_1 = delta_v_inf / delta_i - R_0
rise_time = data[0, i+1]
print("rise_time = ", rise_time)
rising_data = data[2, i+1:]
start_voltage = rising_data[0] - 1

data_adjusted = data[0, i+1:]

def func1(x_input, a, b, c):
    return a*np.exp(-c*(x_input-rise_time))+b

popt, pcov = curve_fit(func1, data_adjusted, rising_data, p0 = [1, 1, 1])
voltage_est = func1(data_adjusted, *popt)
voltage_est_MSE = mean_squared_error(rising_data, voltage_est)
r1c1_est = 1/popt[2]

plt.plot(data_adjusted, rising_data, 'r')
plt.plot(data_adjusted, voltage_est, 'b')
plt.show()
print("popt = ", popt)
print("R0 = %.4f" % R_0)
print("R1 = %.4f" % R_1)
print("R1 * C1 = %.4f" % r1c1_est)
C_1 = r1c1_est / R_1
print("C1 = %.4f" % C_1)
print("voltage_est_MSE = ", voltage_est_MSE)



