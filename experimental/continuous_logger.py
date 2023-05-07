# continuous_logger.py can be used to initiate a logging session using a
# Raspberry Pi Pico W. It reads an analog signal connected to pin 26 and prints
# its value to the terminal.

from machine import ADC
from time import sleep
from time import ticks_us

adc_pin_0 = 26
sensor = ADC(adc_pin_0)
us_in_second = 1000000
# Time period in seconds.
time_period = 0.1


def read_sensor():
    adc_value = sensor.read_u16()
    print(f"sensor value: {adc_value}")
    return adc_value


target_time = ticks_us()
while True:
    target_time += time_period * us_in_second
    adc_value = read_sensor()
    # Try to maintain loop period.
    sleep(max(0, (target_time - ticks_us()) * (1 / us_in_second)))
