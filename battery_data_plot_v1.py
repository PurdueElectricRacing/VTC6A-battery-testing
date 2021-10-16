import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

###40000 till 100000

reader = pd.read_csv(r'VTC6 RPT.csv')
df = pd.DataFrame(reader, columns=['test_time', 'voltage', 'current'])
data = df.to_numpy()

top = np.where(data[:, 0] > 100000)[0][0]
#bottom = np.where(data[:, 0] > 40000)[0][0]  ### finding the needed points
bottom = np.where(data[:, 0] > 0)[0][0]  ### finding the needed points

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


# plt.plot(data[0, :], data[1, :])
# plt.plot(data[0, :], data[2, :])
# plt.plot([data[0][i] for i in swpts], [data[1][i] for i in swpts], 'o')
# plt.show()