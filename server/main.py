from functools import lru_cache
from fastapi import FastAPI, Depends
from src import store, config, log
from typing_extensions import Annotated

log.configure_logging()
app = FastAPI()

@lru_cache()
def get_pull_up_store():
    return store.PullUp()

@lru_cache()
def get_settings():
    return config.Settings()

@app.get("/items/")
async def upsert_pull_up_data(settings: Annotated[config.Settings, 
                                          Depends(get_settings)]):
    pull_up = get_pull_up_store()
    return pull_up.store(spreadsheet_id=settings.spreadsheet_id, 
                         sheet_tab_name=settings.sheet_tab_name)
   