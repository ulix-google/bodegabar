"""Runs the bodegabar application.

The bodegabar application counts pull ups and stores the data in a Google Sheet.
It does so by making use of 3 distinct sensors: a strain gauge, and 2 distance
sensors used to determine the activity of the user. The strain gauge is used to
determine when a user is hanging from the bar, while 1 of the distance sensors
is used to detect the head (of the user when they rise while doing the pull up),
and the other position sensor to detect the hand position of the user on the
bar.

Inputs:
  - Environment variables (which can be provided via a .env file colocated with
    main.py):
    - SPREADSHEET_ID: The ID of the Google Sheet that the app will write to.
    - SHEET_TAB_NAME: The name of the Google Sheet Tab where the data will be
        stored.
"""

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
