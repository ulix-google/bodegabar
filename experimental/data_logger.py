# data_logger.py can be used to initiate a logging session using a Raspberry Pi
# Pico W. It reads an analog signal connected to pin 26, for a given logging
# duration, and outputs the logged data in the form of a text file.

from machine import ADC
from time import sleep
from time import ticks_us

adc_pin_0 = 26
sensor = ADC(adc_pin_0)
us_in_second = 1000000
# Time period in seconds.
time_period = 0.1
# The duration of the logging sesh in seconds. The Raspberry Pi Pico W has a
# limit of 2MB, so each logging session cannot be huge.
logging_length = 60
counter_limit = logging_length / time_period
file = open("data.txt", "w")


def read_sensor():
    adc_value = sensor.read_u16()
    print(f"sensor value: {adc_value}")
    return adc_value


loop_counter = 0
target_time = ticks_us()
while loop_counter < counter_limit:
    target_time += time_period * us_in_second
    adc_value = read_sensor()
    file.write(str(adc_value) + "\n")
    loop_counter += 1
    # Try to maintain loop period.
    sleep(max(0, (target_time - ticks_us()) * (1 / us_in_second)))

file.close()
