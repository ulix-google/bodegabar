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


def read_sensor():
    adc_value = channel.value
    print(f"sensor value: {adc_value}")
    return adc_value


target_time = time()
while True:
    target_time += time_period
    adc_value = read_sensor()
    # Try to maintain loop period.
    sleep(max(0, (target_time - time())))
