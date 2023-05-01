import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import mplcyberpunk


class DataFile:
    def __init__(self, filename: str, plotColor: str) -> None:
        self.plotColor = plotColor
        self.filename = filename


# Time period in seconds.
time_period = 0.1
data_files = [
    DataFile("sunny_afternoon_direct_light.txt", "gold"),
    DataFile("sunny_afternoon_hard_blinds.txt", "orange"),
    DataFile("sunny_afternoon_light_blinds.txt", "lightyellow"),
    DataFile("night_no_indoor_lights.txt", "violet"),
    DataFile("night_all_indoor_lights_on.txt", "mediumpurple"),
]

# Style it up.
plt.style.use("cyberpunk")
plt.xlabel("Time (s)")
plt.ylabel("ADC signal (0 to 65535)")

sensor_data = defaultdict(list)
for data_file in data_files:
    with open(data_file.filename) as file:
        for string_value in file:
            sensor_data[data_file.filename].append(float(string_value))
    time_vector = np.arange(
        0.0, len(sensor_data[data_file.filename]) * time_period, time_period
    )
    len(time_vector)
    plt.plot(
        time_vector,
        sensor_data[data_file.filename],
        label=data_file.filename,
        color=data_file.plotColor,
    )


plt.xlim([0, 9])
plt.legend(loc="upper left")
# Make it beautiful.
mplcyberpunk.add_glow_effects()
plt.show()
