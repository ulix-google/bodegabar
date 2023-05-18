import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

from . import sma

RIGHT_HAND_SIGNAL = "right_hand_signal"
HEAD_SIGNAL = "head_signal"
STRAIN_GAUGE_SIGNAL = "strain_gauge_signal"


class Sensors:
    def __init__(self, time_period, buffer_window_length=3):
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        cs = digitalio.DigitalInOut(board.D5)
        mcp = MCP.MCP3008(spi, cs)
        self.analog_signals = {}
        self.analog_signals[RIGHT_HAND_SIGNAL] = AnalogIn(mcp, MCP.P0)
        self.analog_signals[HEAD_SIGNAL] = AnalogIn(mcp, MCP.P1)
        self.analog_signals[STRAIN_GAUGE_SIGNAL] = AnalogIn(mcp, MCP.P2)
        self.sma = {}
        for signals in self.analog_signals:
            self.sma[signals] = sma.SMA(buffer_window_length, time_period)

    def handle_samples(self):
        for signals in self.analog_signals:
            self.sma[signals].insert(self.analog_signals[signals].value)
