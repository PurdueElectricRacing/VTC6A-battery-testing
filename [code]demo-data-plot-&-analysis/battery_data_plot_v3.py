import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

###40000 till 100000

reader = pd.read_csv(r'../early-testing-&-demo-data/VTC6 RPT.csv')
df = pd.DataFrame(reader, columns=['test_time', 'voltage', 'current'])
data = df.to_numpy()

top = np.where(data[:, 0] > 48400)[0][0]
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
while(data[1,i] >= data[1, i+1]):
    print(data[1, i])
    i = i+1
print(i)
rising_data = data[1, i:]
start_voltage = rising_data[0] - 1
#print(rising_data)

data_adjusted = data[0, i:] - data[0, 0]
constant = 3
rising_data_trimmed = (4091 - rising_data)
#print(rising_data_trimmed)
#print(rising_data_trimmed)
log_rising_voltage_data_trimmed = np.log(rising_data_trimmed)
#print(log_rising_voltage_data_trimmed)

# curve_fit = np.polyfit(data[0,i:], log_rising_voltage_data_trimmed, 1)
curve_fit = np.polyfit(data_adjusted, log_rising_voltage_data_trimmed, 1)
data = data.astype(np.float128)
#curve_fit[0] = -0.006
#curve_fit[1] = 4
print(curve_fit[0], curve_fit[1])

# curve_fit[0] = -0.007 curve_fit[1] = 4
v_estimate = -1 * np.exp(curve_fit[1])*np.exp(curve_fit[0]*data_adjusted) + 4090
plt.plot(data_adjusted, rising_data, "r")
plt.plot(data_adjusted, v_estimate, "b")
plt.show()


plt.plot(data_adjusted, log_rising_voltage_data_trimmed)
plt.show()





# plt.plot(data[0, :], data[1, :])
# plt.plot(data[0, :], data[2, :])
# plt.plot([data[0][i] for i in swpts], [data[1][i] for i in swpts], 'o')
# plt.show()