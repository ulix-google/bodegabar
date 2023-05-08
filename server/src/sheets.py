import google.auth
from googleapiclient import discovery

class Sheets:
    def __init__(self):
        credentials, _ = google.auth.default()
        service_resource = discovery.build('sheets',
                                           'v4',
                                           credentials=credentials)
        self.sheet_service = service_resource.spreadsheets()

    def query_sheet(self, sheet_tab_name: str, spreadsheet_id: str) -> str:
        sheet_range = sheet_tab_name + "!M3:M23"
        result = self.sheet_service.values().get(
            spreadsheetId=spreadsheet_id, 
            range=sheet_range).execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
            return ""
        concat_values = ""
        for row in values:
            concat_values += ' '.join(row)
            print(f"row: {row}")
        return concat_values
