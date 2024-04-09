import json
from models.classes_models import Classes, Class

def get_classes_db(file_path) -> dict:
    with open(file_path) as f:
        data = Classes(**json.load(f))
        return data.model_dump()

def get_class_by_id(classes_list: list[dict], class_id: int):
    if type(class_id) != int or class_id < 0:
        raise ValueError("class id must be a positive integer")
    
    if type(classes_list) != list:
        raise ValueError(f"Classes list must be a list not {type(classes_list)}")
    
    if len(classes_list) == 0:
        raise ValueError("classes list is empty")

    for c in classes_list:
        if c["id"] == class_id:
            target_class = Class(**c)
            return target_class.model_dump()
    return None
