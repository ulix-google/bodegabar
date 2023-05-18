import os
from dotenv import load_dotenv

from src import sensor, detect, store


class Config:
    def __init__(self):
        # Load a .env file which should hold variables for the pull up service in the
        # following format:
        #   SPREADSHEET_ID="example_spreadsheet_id"
        #   SHEET_TAB_NAME="example_sheet_tab_name"
        load_dotenv()
        SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
        SHEET_TAB_NAME = os.getenv("SHEET_TAB_NAME")
        pull_up_service = store.PullUp(
            sheet_tab_name=SHEET_TAB_NAME,
            spreadsheet_id=SPREADSHEET_ID,
        )
        # Loop time period in seconds.
        self.time_period = 0.05
        # Simple-Moving-Average buffer window length in seconds.
        buffer_window_length = 2
        self.sensors = sensor.Sensors(
            time_period=self.time_period,
            buffer_window_length=buffer_window_length,
        )
        self.detector = detect.Detector(
            sensors=self.sensors,
            pull_up_service=pull_up_service,
        )
