import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error

### overview: crop from 44884 till 45500

reader = pd.read_csv(r'../early-testing-&-demo-data/VTC6 RPT.csv')
df = pd.DataFrame(reader, columns=['test_time', 'voltage', 'current'])
data = df.to_numpy()

top = np.where(data[:, 0] > 45500)[0][0] # original crop: 48400
#bottom = np.where(data[:, 0] > 40000)[0][0]  ### finding the needed points
bottom = np.where(data[:, 0] > 44884)[0][0]  ### finding the needed points

data = data[bottom:top, :]  ### slicing the requireed dataset

data = data.T  ###transpose

swpts = []

for i in range(len(data[0]) - 1):  # finding the swich points
    if abs(data[2, i + 1] - data[2, i]) > 100:
        swpts.append(i)

print(len(swpts))

fig, ax1 = plt.subplots()

color_red = 'tab:red'
ax1.set_xlabel('time(s)')
ax1.set_ylabel('voltage(mV)', color=color_red)
ax1.scatter(data[0, :], data[1, :], color=color_red, s=0.5)
ax1.tick_params(axis='y', labelcolor=color_red)

ax2 = ax1.twinx()

color_blue = 'tab:blue'
ax2.set_ylabel('current(mA)', color=color_blue)
ax2.scatter(data[0, :], data[2, :], color=color_blue, s=0.5)
ax2.tick_params(axis='y', labelcolor=color_blue)

fig.tight_layout()
plt.show()

# rising edge detection

i = 1
while(data[1,i] >= data[1, i+1] - 10):
    #print(data[1, i])
    i = i+1
#print(i)
rising_data = data[1, i+1:]
start_voltage = rising_data[0] - 1

data_adjusted = data[0, i+1:]

def func1(x_input, a, b, c):
    return a*np.exp(-c*(x_input-44892))+b

popt, pcov = curve_fit(func1, data_adjusted, rising_data, p0 = [4e+3, 1, 4.2e-2])
voltage_est = func1(data_adjusted, *popt)
voltage_est_MSE = mean_squared_error(rising_data, voltage_est)
r1c1_est = 1/popt[2]

plt.plot(data_adjusted, rising_data, 'r')
plt.plot(data_adjusted, voltage_est, 'b')
plt.show()
print("popt = ", popt)
print("R1 * C1 = ", r1c1_est)
print("voltage_est_MSE = ", voltage_est_MSE)



