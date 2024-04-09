from typing import List
from pydantic import BaseModel

class Class(BaseModel):
    id: int
    name: str
    teacher: str
    topic: str

class Classes(BaseModel):
    classes: List[Class]