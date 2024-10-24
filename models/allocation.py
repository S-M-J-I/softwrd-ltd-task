from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
from datetime import datetime


class Allocation(BaseModel):
    vehicle: str
    employee: str
    booked_at: Optional[datetime] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
