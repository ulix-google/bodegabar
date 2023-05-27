from enum import Enum
from pydantic import BaseModel


class PullUpType(Enum):
    """Type of pull up, e.g. Pull up vs. Chin Up."""

    PullUp = 1
    ChinUp = 2


class PullUpBarRequest(BaseModel):
    date: str
    pull_up_count: int = 0
    chin_up_count: int = 0
    pull_up_type: PullUpType = PullUpType.PullUp
