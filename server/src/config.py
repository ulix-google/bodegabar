from pydantic import BaseSettings


class Settings(BaseSettings):
    """Holds app settings.

    Holds the configuration settings for the application. Do not modify the
    values to this class, instead: create a `.env` file and store it on the
    same directory as `main.py`, i.e. `bodegabar/server/.env`.

    Args:
        None
    Returns:
        None
    """
    spreadsheet_id: str = "default-spreadsheet-id"
    sheet_tab_name: str = "default-sheet-tab-name"

    class Config:
        env_file = ".env"