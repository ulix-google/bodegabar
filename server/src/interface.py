from pydantic import BaseModel

class PullUpBarRequest(BaseModel):
    date: str
    pull_up_count: int = 0
    chin_up_count: int = 0