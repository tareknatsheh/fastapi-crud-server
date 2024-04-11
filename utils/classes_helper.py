import json
from models.classes_models import Class

def get_classes_db(file_path) -> dict:
    with open(file_path) as f:
        return json.load(f)


    
def validate_class_list(classes_list):
    if type(classes_list) != list:
        raise ValueError(f"Classes list must be a list not {type(classes_list)}")
    if len(classes_list) == 0:
        raise ValueError("classes list is empty")


def get_class_by_id(classes_list: list[dict], class_id: int) -> Class | None:
    validate_class_list(classes_list)
    if not isinstance(class_id, int) or class_id < 0:
        raise ValueError("ID must be an integer")
    for c in classes_list:
        if c["id"] == class_id:
            target_class = Class(**c)
            return target_class
    return None
