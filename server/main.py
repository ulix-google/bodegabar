from functools import lru_cache

from fastapi import FastAPI, Depends
from src import sheets, config
from typing_extensions import Annotated

app = FastAPI()

@lru_cache()
def get_sheet_client():
    return sheets.Sheets()

@lru_cache()
def get_settings():
    return config.Settings()

@app.get("/items/")
async def upsert_pull_up_data(settings: Annotated[config.Settings, 
                                          Depends(get_settings)]):
    sheet = get_sheet_client()
    return sheet.query_sheet(spreadsheet_id=settings.spreadsheet_id, 
                             sheet_tab_name=settings.sheet_tab_name)
