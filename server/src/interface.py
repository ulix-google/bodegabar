from pydantic import BaseModel

class PullUpBarUpdate(BaseModel):
    date: str
    pull_up_count: int = 0
    chin_up_count: int = 0