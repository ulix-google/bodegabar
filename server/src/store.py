import logging
import google.auth
from datetime import datetime
from googleapiclient import discovery

from . import utils, interface


class PullUp:
    """Storage related functionality for Pull Ups.

    PullUp has functionality for handling the storage of pull up data by
    persisting it in a Google Sheet in the appropriate cell(s).

    Attributes:
        sheet_tab_name: A string representing the name of the tab sheet in
          which pull up data is stored.
        spreadsheet_id: A string representing the spreadsheet ID which
          contains the sheet which stores pull up data.
    """

    def __init__(self, sheet_tab_name: str, spreadsheet_id: str):
        """Initializes the instance with the provided Google Sheet metadata.

        Args:
          sheet_tab_name: The name of the tab sheet in which pull up data is
            stored.
          spreadsheet_id: The spreadsheet ID which contains the sheet which
            stores pull up data.
        """
        credentials, _ = google.auth.default()
        service_resource = discovery.build("sheets", "v4", credentials=credentials)
        self.sheet_service = service_resource.spreadsheets()
        self.FIRST_DATE_COLUMN = "A"
        self.FIRST_DATE_ROW = "2"
        self._sheet_tab_name = sheet_tab_name
        self._spreadsheet_id = spreadsheet_id

    def store(
        self,
        pull_up_bar_request: interface.PullUpBarRequest,
    ) -> str:
        """Handles a pull up bar request.

        store handles a pull up bar request, by figuring out the cell that
        will be the recepeint of the updates, and then upserting the pull up
        data.

        Args:
            pull_up_bar_request: a pull up bar request.

        Returns:
            TBD
        """
        # The sheet service expects a range in the form of:
        # <Sheet Tab Name>!<Cell Range>.
        # Example 1: Exercise!A2
        # Example 2: Project!A2:B4
        sheet_range = (
            self._sheet_tab_name + "!" + self.FIRST_DATE_COLUMN + self.FIRST_DATE_ROW
        )
        result = (
            self.sheet_service.values()
            .get(spreadsheetId=self._spreadsheet_id, range=sheet_range)
            .execute()
        )
        values = result.get("values", [])
        first_date = self._validate_first_date_value(values)

        days_delta = self._compute_day_difference(
            first_date=first_date, update_date=pull_up_bar_request.date
        )

        self._upsert_pull_up_data(
            days_delta=days_delta,
            pull_up_count=pull_up_bar_request.pull_up_count,
            pull_up_type=pull_up_bar_request.pull_up_type,
        )
        return first_date

    def _upsert_pull_up_data(
        self,
        days_delta: int,
        pull_up_count: int,
        pull_up_type: interface.PullUpType = interface.PullUpType.PullUp,
    ) -> None:
        # Move to the right column relative to the `Date` column, which
        # corresponds to the Pull-Up count column.
        right_column = chr(ord(self.FIRST_DATE_COLUMN) + pull_up_type.value)
        pull_up_cell = right_column + str(days_delta + int(self.FIRST_DATE_ROW))
        logging.getLogger().info(f"Writing to cell: {pull_up_cell}")
        pull_up_range = self._sheet_tab_name + "!" + pull_up_cell
        stored_pull_ups = self._get_stored_pull_ups(pull_up_range)
        logging.getLogger().info(f"Stored pull ups read: {stored_pull_ups}")
        values = [[pull_up_count + stored_pull_ups]]
        body = {"values": values}
        result = (
            self.sheet_service.values()
            .update(
                spreadsheetId=self._spreadsheet_id,
                range=pull_up_range,
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )
        logging.getLogger().info(f"Sheets API response after writing: {result}")
        return

    def _get_stored_pull_ups(self, pull_up_range: str) -> int:
        result = (
            self.sheet_service.values()
            .get(spreadsheetId=self._spreadsheet_id, range=pull_up_range)
            .execute()
        )
        values = result.get("values", [])
        if not values:
            logging.getLogger().error(f"Failed to read a value.")
            return 0

        if len(values) != 1:
            logging.getLogger().error(
                f"Expected 1 column in `values`, instead got `values`: {values}"
            )
            return 0

        row = values[0]
        if len(row) != 1:
            logging.getLogger().error(
                f"Expected 1 column in `row`, instead got `row`: {row}"
            )
            return 0

        stored_pull_ups = row[0]
        if stored_pull_ups == "":
            return 0
        return int(stored_pull_ups)

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
                f"Failed to read a value in {self.FIRST_DATE_COLUMN}{self.FIRST_DATE_ROW}"
            )
            return ""

        if len(values) != 1:
            logging.getLogger().error(
                f"Expected 1 column in `values`, instead got `values`: {values}"
            )
            return ""

        row = values[0]
        if len(row) != 1:
            logging.getLogger().error(
                f"Expected 1 column in `row`, instead got `row`: {row}"
            )
            return ""

        first_date = row[0]
        if not utils.is_date(first_date):
            logging.getLogger().error(f"Expected a date, instead got: {first_date}")
            return ""

        logging.getLogger().info(f"First date read: {first_date}")
        return first_date
