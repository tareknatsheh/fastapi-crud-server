from pydantic import BaseModel, validator

class Student(BaseModel):
    name: str
    id: int
    age: int
    classes: list[str]

    @validator("id")
    def validate_id(cls, value):
        if value < 0:
            raise ValueError("Student id must be a positive integer")
        return value
    
    @validator("age")
    def validate_age(cls, value):
        if value < 0:
            raise ValueError("Student age must be a positive integer")
        return value
    
    @validator("name")
    def validate_name(cls, value):
        if len(value) < 2:
            raise ValueError("Student name must be at least 1 character")
        return value