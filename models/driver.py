from pydantic import BaseModel
from bson import ObjectId


class Driver(BaseModel):
    name: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
