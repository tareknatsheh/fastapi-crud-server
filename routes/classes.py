from traceback import print_tb
from fastapi import APIRouter, Request
from utils.decorators import handle_errors, log_it
import utils.classes_helper as c
from models.classes_models import Classes, Class

router = APIRouter()
CLASSES_DB = "./data/classes_db.json"

@router.post("/add-class-to-student")
@handle_errors
@log_it
def add_class_to_student(request: Request,class_id: int, student_id: int):
    # get classes db
    data = c.get_classes_db(CLASSES_DB)

    if "classes" not in data:
        raise Exception("Classes db must have a 'classes' KVP")
    
    classes_list = data["classes"]
    # get class object by id
    target_class = c.get_class_by_id(classes_list, class_id)

    print(target_class)
    
    # get student object
    # add class to student
    # update students db
    
    return {"message": f"class id is {class_id}, and student id is {student_id}"}