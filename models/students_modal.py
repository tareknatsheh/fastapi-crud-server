from pydantic import BaseModel

class Student(BaseModel):
    name: str
    id: int
    age: int
    classes: list[str]