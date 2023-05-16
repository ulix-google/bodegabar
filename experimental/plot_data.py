import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import mplcyberpunk
from typing import List


class DataFile:
    def __init__(self, filename: str, plotColor: List[str]) -> None:
        self.plotColor = plotColor
        self.filename = filename


# Time period in seconds.
time_period = 0.1
data_files = [
    DataFile(
        r"data\rp_adc_night_all_indoor_lights.txt",
        ["gold", "orange", "violet"],
    ),
]

# Style it up.
plt.style.use("cyberpunk")
plt.xlabel("Time (s)")
plt.ylabel("ADC signal (0 to 65535)")


def normalize_time(time_vector):
    start_time = time_vector[0]
    for i in range(len(time_vector)):
        time_vector[i] = time_vector[i] - start_time
    return time_vector


sensor_data = defaultdict(list)
time_vector = []
for data_file in data_files:
    with open(data_file.filename) as file:
        header = True
        headers = ["", "", ""]
        for string_values in file:
            if header:
                headers = string_values.split(",")
                header = False
                continue
            values = string_values.split(",")
            time_vector.append(float(values[0]))
            sensor_data[headers[1]].append(float(values[1]))
            sensor_data[headers[2]].append(float(values[2]))
            sensor_data[headers[3]].append(float(values[3]))
    time_vector = normalize_time(time_vector)
    signal_number = 0
    for signal_name, signal_values in sensor_data.items():
        plt.plot(
            time_vector,
            signal_values,
            label=signal_name,
            color=data_file.plotColor[signal_number],
        )
        signal_number += 1


plt.xlim([0, 30])
plt.ylim([-5000, 85000])
plt.legend(loc="upper left")
# Make it beautiful.
mplcyberpunk.add_glow_effects()
plt.show()
