from time import sleep, time

import config
from src import log

log.configure_logging()
cfg = config.Config()
target_time = time()


# Duration of the logging session in seconds.
logging_length = 60
counter_limit = logging_length / cfg.time_period
file = open("data.txt", "w")
file.write("Time,Right Hand Signal,Head Signal,Strain Gauge Signal\n")
loop_counter = 0
target_time = time()
while loop_counter < counter_limit:
    target_time += cfg.time_period
    cfg.sensors.handle_samples()
    if cfg.sensors.sma["right_hand_signal"].average is not None:
        file.write(
            f"{time()},{cfg.sensors.sma['right_hand_signal'].average},{cfg.sensors.sma['head_signal'].average},{cfg.sensors.sma['strain_gauge_signal'].average}\n"
        )
    loop_counter += 1
    # Try to maintain loop period.
    cfg.detector.handle()
    sleep(max(0, (target_time - time())))

file.close()
