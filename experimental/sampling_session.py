import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from time import sleep, time

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
right_hand_signal = AnalogIn(mcp, MCP.P0)
head_signal = AnalogIn(mcp, MCP.P1)
strain_gauge_signal = AnalogIn(mcp, MCP.P2)

# Time period in seconds.
time_period = 0.05
# Duration of the logging session in seconds.
logging_length = 60
counter_limit = logging_length / time_period
file = open("data.txt", "w")


# def print_sensor_values():
# print(f"RHS: {right_hand_signal.value}, HS: {head_signal.value}")


loop_counter = 0
target_time = time()
file.write("Time,Right Hand Signal,Head Signal,Strain Gauge Signal\n")
while loop_counter < counter_limit:
    target_time += time_period
    # print_sensor_values()
    file.write(
        f"{time()},{right_hand_signal.value},{head_signal.value},{strain_gauge_signal.value}\n"
    )
    loop_counter += 1
    # Try to maintain loop period.
    sleep(max(0, (target_time - time())))

file.close()
