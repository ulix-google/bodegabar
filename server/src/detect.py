import logging
from datetime import datetime

from . import sensor, store, interface

# Slope thresholds in ADC counts (0 to 65k).
RIGHT_HAND_THRESHOLD = 15000
HEAD_THRESHOLD = 15000
STRAIN_GAUGE_THRESHOLD = 55000


class Detector:
    def __init__(self, sensors: sensor.Sensors, pull_up_service: store.PullUp):
        self.sensors = sensors
        self.previous_head_signal = None
        self.previous_strain_signal = None
        self.pull_up_count = 0
        self.pull_up_service = pull_up_service

    def _store_state(self):
        self.previous_head_signal = self.sensors.sma[sensor.HEAD_SIGNAL].average
        self.previous_strain_signal = self.sensors.sma[
            sensor.STRAIN_GAUGE_SIGNAL
        ].average

    def handle(self):
        if self.previous_head_signal is None:
            self._store_state()
            return

        if (
            self.previous_head_signal > HEAD_THRESHOLD
            and self.sensors.sma[sensor.HEAD_SIGNAL].average < HEAD_THRESHOLD
            and self.sensors.sma[sensor.RIGHT_HAND_SIGNAL].average
            > RIGHT_HAND_THRESHOLD
            and self.sensors.sma[sensor.STRAIN_GAUGE_SIGNAL].average
            < STRAIN_GAUGE_THRESHOLD
        ):
            self.pull_up_count += 1
            logging.getLogger().info(
                f"Push-up detected! Count so far: {self.pull_up_count}."
            )
            self._store_state()
            return

        if (
            self.previous_strain_signal < STRAIN_GAUGE_THRESHOLD
            and self.sensors.sma[sensor.STRAIN_GAUGE_SIGNAL].average
            > STRAIN_GAUGE_THRESHOLD
        ):
            logging.getLogger().info(
                f"Logging a total of {self.pull_up_count} pull ups."
            )
            self._store_state()
            pull_up_bar_request = interface.PullUpBarRequest(
                date=datetime.today().strftime("%m/%d/%y"),
                pull_up_count=self.pull_up_count,
            )
            if self.pull_up_count > 0:
                self.pull_up_service.store(pull_up_bar_request)
            self.pull_up_count = 0
            return

        self._store_state()
        return
