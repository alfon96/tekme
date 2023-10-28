from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class KidLog(BaseModel):
    name: str
    classes: int
    breaks: int
    teacher: str
    date: datetime
    detail: Optional[str] = None
