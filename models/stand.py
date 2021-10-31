from pydantic import BaseModel
from typing import Optional


class Stand(BaseModel):
    name: str
    address: str
    platform: str
    available: bool


class StandUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    platform: Optional[str] = None
    available: Optional[bool] = None
