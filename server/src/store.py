import logging
import google.auth
from . import utils
from googleapiclient import discovery

class PullUp:
    def __init__(self):
        credentials, _ = google.auth.default()
        service_resource = discovery.build('sheets',
                                           'v4',
                                           credentials=credentials)
        self.sheet_service = service_resource.spreadsheets()
        self.FIRST_DATE_CELL = "A2"

    def store(self, sheet_tab_name: str, spreadsheet_id: str) -> str:
        sheet_range = sheet_tab_name + "!" + self.FIRST_DATE_CELL
        result = self.sheet_service.values().get(
            spreadsheetId=spreadsheet_id, 
            range=sheet_range).execute()
        values = result.get('values', [])
        first_date = self._validate_first_date_value(values)
        
        logging.getLogger().info(f"First date read: {first_date}")
        return first_date
    
    def _validate_first_date_value(self, values) -> str:
        if not values:
            logging.getLogger().error(
                f"Expected a date on cell: {self.FIRST_DATE_CELL}, instead got: {values}")
            return ""
        
        if len(values) != 1:
            logging.getLogger().error(
                f"Expected 1 column in `values`, instead got `values`: {values}")
            return ""
        
        value = values[0]
        if len(value) != 1:
            logging.getLogger().error(
                f"Expected 1 row in `value`, instead got `value`: {value}")
            return ""
        
        first_date = value[0]
        if not utils.is_date(first_date):
            logging.getLogger().error(
                f"Expected a date, instead got: {first_date}")
            return ""
