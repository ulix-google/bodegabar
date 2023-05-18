import logging
from time import sleep, time

import config
from src import log

log.configure_logging()
cfg = config.Config()
target_time = time()

while True:
    try:
        target_time += cfg.time_period
        cfg.sensors.handle_samples()
        cfg.detector.handle()
        # Try to maintain loop period.
        sleep(max(0, (target_time - time())))
    except Exception as err:
        logging.getLogger().error(f"Unexpected {err=}, {type(err)=}")
