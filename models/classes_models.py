from typing import List
from pydantic import BaseModel, validator

class Class(BaseModel):
    id: int
    name: str
    teacher: str
    topic: str

    @validator("id")
    def validate_id(cls, value):
        if type(value) != int or value < 0:
            raise ValueError("Class id must be a positive integer")
        return value
