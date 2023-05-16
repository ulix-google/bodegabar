import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from time import sleep, time

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
channel = AnalogIn(mcp, MCP.P0)
# Time period in seconds.
time_period = 0.1
# The duration of the logging sesh in seconds. The Raspberry Pi Pico W has a
# limit of 2MB, so each logging session cannot be huge.
logging_length = 60
counter_limit = logging_length / time_period
file = open("data.txt", "w")


def read_sensor():
    adc_value = channel.value
    print(f"sensor value: {adc_value}")
    return adc_value


loop_counter = 0
target_time = time()
while loop_counter < counter_limit:
    target_time += time_period
    adc_value = read_sensor()
    file.write(str(adc_value) + "\n")
    loop_counter += 1
    # Try to maintain loop period.
    sleep(max(0, (target_time - time())))

file.close()
