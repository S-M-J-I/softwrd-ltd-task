from pydantic import BaseModel
from typing import Optional
from bson import ObjectId


class Vehicle(BaseModel):
    name: str
    type: str
    num_plate: str
    driver: Optional[ObjectId] = None
    allocated: Optional[bool] = False

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
