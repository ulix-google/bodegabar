import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import mplcyberpunk
from typing import List


class DataFile:
    def __init__(self, filename: str, plotColor: List[str]) -> None:
        self.plotColor = plotColor
        self.filename = filename


class SMA:
    def __init__(self, buffer_window_length: float, time_period: float) -> None:
        self.buffer = [0] * int(buffer_window_length / time_period)
        self.buffer_ready = False
        self.buffer_pointer = 0
        self.cum_sum = 0
        self.average = None

    def insert(self, value) -> None:
        self.cum_sum += value
        self.cum_sum -= self.buffer[self.buffer_pointer]
        self.buffer[self.buffer_pointer] = value
        self.buffer_pointer += 1
        if self.buffer_pointer >= len(self.buffer):
            self.buffer_pointer = 0
            if self.buffer_ready is False:
                self.buffer_ready = True
        self._compute_average()

    def _compute_average(self):
        if self.buffer_ready:
            self.average = self.cum_sum / len(self.buffer)


# Time period in seconds.
time_period = 0.05
data_files = [
    DataFile(
        r"data\rp_averaged_night_all_indoor_lights_run_010.txt",
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
headers = ["", "", ""]
for data_file in data_files:
    with open(data_file.filename) as file:
        header = True
        for string_values in file:
            if header:
                headers = string_values.split(",")
                header = False
                continue
            values = string_values.split(",")
            time_vector.append(float(values[0]))
            for i in range(1, len(headers)):
                sensor_data[headers[i]].append(float(values[i]))
    time_vector = normalize_time(time_vector)
    signal_number = 0
    for signal_name, signal_values in sensor_data.items():
        plt.plot(
            time_vector,
            signal_values,
            label=signal_name,
            color=data_file.plotColor[signal_number],
            marker="o",
        )
        signal_number += 1

buffer_window_length = 3
moving_averages = {}
for header in headers:
    moving_averages[header] = SMA(buffer_window_length, time_period)

average_time_vector = []
averaged_data = defaultdict(list)
for i in range(len(sensor_data[headers[1]])):
    for j in range(1, len(headers)):
        moving_averages[headers[j]].insert(sensor_data[headers[j]][i])
        if moving_averages[headers[j]].average is not None:
            if j == 1:
                average_time_vector.append(time_vector[i])
            averaged_data[headers[j]].append(moving_averages[headers[j]].average)

# for signal_name, _ in sensor_data.items():
#     plt.plot(
#         average_time_vector,
#         averaged_data[signal_name],
#         label="Averaged" + signal_name,
#     )


for j in range(1, len(headers)):
    true_mean = sum(moving_averages[headers[j]].buffer) / len(
        moving_averages[headers[j]].buffer
    )
    print(f"{headers[j]} sma: {moving_averages[headers[j]].average}")
    print(f"{headers[j]} true_mean: {true_mean}")
    print(f"{headers[j]} error: {abs(true_mean - moving_averages[headers[j]].average)}")

# plt.xlim([0, 60])
plt.ylim([-5000, 85000])
plt.legend(loc="upper left")
# Make it beautiful.
mplcyberpunk.add_glow_effects()
plt.show()
