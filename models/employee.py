from pydantic import BaseModel, Field
from models.py_obj import PyObjectId
from typing import Optional


class Employee(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
