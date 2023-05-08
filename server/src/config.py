from pydantic import BaseSettings


class Settings(BaseSettings):
    spreadsheet_id: str = "default-spreadsheet-id"
    sheet_tab_name: str = "default-sheet-tab-name"

    class Config:
        env_file = ".env"