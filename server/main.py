from functools import lru_cache
from fastapi import FastAPI, Depends
from src import store, config, log, interface
from typing_extensions import Annotated

log.configure_logging()
app = FastAPI()

@lru_cache()
def get_pull_up_store(sheet_tab_name: str, 
                      spreadsheet_id: str):
    return store.PullUp(spreadsheet_id=spreadsheet_id,
                        sheet_tab_name=sheet_tab_name)

@lru_cache()
def get_settings():
    return config.Settings()

@app.get("/items/")
async def upsert_pull_up_data(pull_up_bar_request: interface.PullUpBarRequest | None = None,
                              settings: Annotated[config.Settings, 
                                          Depends(get_settings)] = None):
    pull_up = get_pull_up_store(spreadsheet_id=settings.spreadsheet_id,
                                sheet_tab_name=settings.sheet_tab_name)
    pull_up_bar_request = interface.PullUpBarRequest(
        date="5/7/23",
        pull_up_count=17)
    return pull_up.store(pull_up_bar_request=pull_up_bar_request)
   