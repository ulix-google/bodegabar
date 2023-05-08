import logging
import google.auth
from googleapiclient import discovery
from datetime import datetime

from . import utils, interface

class PullUp:
    def __init__(self,
                 sheet_tab_name: str, 
                 spreadsheet_id: str):
        credentials, _ = google.auth.default()
        service_resource = discovery.build('sheets',
                                           'v4',
                                           credentials=credentials)
        self.sheet_service = service_resource.spreadsheets()
        self.FIRST_DATE_COLUMN = "A"
        self.FIRST_DATE_ROW = "2"
        self._sheet_tab_name = sheet_tab_name
        self._spreadsheet_id = spreadsheet_id

    def store(self,
              pull_up_bar_update: interface.PullUpBarUpdate) -> str:
        # The sheet service expects a range in the form of:
        # <Sheet Tab Name>!<Cell Range>.
        # Example 1: Exercise!A2
        # Example 2: Project!A2:B4
        sheet_range = (self._sheet_tab_name 
                       + "!" 
                       + self.FIRST_DATE_COLUMN
                       + self.FIRST_DATE_ROW)
        result = self.sheet_service.values().get(
            spreadsheetId=self._spreadsheet_id, 
            range=sheet_range).execute()
        values = result.get('values', [])
        first_date = self._validate_first_date_value(values)
        
        days_delta = self._compute_day_difference(
            first_date=first_date,
            update_date=pull_up_bar_update.date)
        
        self._upsert_pull_up_data(
            days_delta=days_delta,
            pull_up_count=pull_up_bar_update.pull_up_count)
        return first_date
    
    def _upsert_pull_up_data(self, 
                              days_delta: int, 
                              pull_up_count: int) -> None:
        # Move to the right column relative to the `Date` column.
        right_column = chr(ord(self.FIRST_DATE_COLUMN) + 1)
        pull_up_cell = right_column + str(days_delta + int(self.FIRST_DATE_ROW))
        logging.getLogger().info(f"Writing to cell: {pull_up_cell}")
        pull_up_range = (self._sheet_tab_name 
                       + "!" 
                       + pull_up_cell)
        values = [[pull_up_count]]
        body = {'values': values}
        result = self.sheet_service.values().update(
            spreadsheetId=self._spreadsheet_id, range=pull_up_range,
            valueInputOption="USER_ENTERED", body=body).execute()
        logging.getLogger().info(f"Sheets API response after writing: {result}")
        return
    
    def _compute_day_difference(self, first_date: str, update_date: str) -> int:
        DATE_FORMAT = "%m/%d/%y"
        d0 = datetime.strptime(first_date, DATE_FORMAT)
        d1 = datetime.strptime(update_date, DATE_FORMAT)
        days_delta = d1 - d0
        logging.getLogger().info(f"Days between first and update date: {days_delta}")
        return days_delta.days
    
    def _validate_first_date_value(self, values) -> str:
        if not values:
            logging.getLogger().error(
                f"Failed to read a value in {self.FIRST_DATE_COLUMN}{self.FIRST_DATE_ROW}")
            return ""
        
        if len(values) != 1:
            logging.getLogger().error(
                f"Expected 1 column in `values`, instead got `values`: {values}")
            return ""
        
        row = values[0]
        if len(row) != 1:
            logging.getLogger().error(
                f"Expected 1 column in `row`, instead got `row`: {row}")
            return ""
        
        first_date = row[0]
        if not utils.is_date(first_date):
            logging.getLogger().error(
                f"Expected a date, instead got: {first_date}")
            return ""
        
        logging.getLogger().info(f"First date read: {first_date}")
        return first_date
