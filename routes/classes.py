from turtle import update
from fastapi import APIRouter, Request
from models.students_models import Student
from models.classes_models import Class
from utils.decorators import handle_errors, log_it
import utils.classes_helper as c
from utils.db_helper import get_all_students, update_students_list, get_student_by_id
from decouple import config


router = APIRouter()
CLASSES_DB = "./data/classes_db.json"
DB_FILEPATH = config("DB_FILEPATH")


@router.post("/add-class-to-student")
@handle_errors
@log_it
def add_class_to_student(request: Request,class_id: int, student_id: int):
    """Add a class to a student's classes list

    Args:
        class_id (int): id of the class to be added
        student_id (int): id of student to add the class to

    Returns:
        student: the Student object
    """

    # get classes db
    data: dict = c.get_classes_db(CLASSES_DB)
    if "classes" not in data:
        raise Exception("Classes db must have a 'classes' key")
    classes_list: list = data["classes"]

    # get class object by id
    target_class: Class | None = c.get_class_by_id(classes_list, class_id)

    if not target_class:
        raise ValueError(f"Can't find the class with id {class_id}")
    
    # get student object
    all_students = get_all_students(DB_FILEPATH)
    index, target_student = get_student_by_id(DB_FILEPATH, all_students, student_id)

    # check if student already enrolled in the class
    if not target_student.classes:
        raise ValueError(f"student with id {student_id} does not have a 'classes' list kvp")
    
    # add class to student
    if target_class.name in target_student.classes:
        return {"message": f"Student {target_student.name} is already enrolled in class {target_class.name}."}
    target_student.classes.append(target_class.name)
    # update students db
    all_students[index] = target_student.model_dump()

    update_res = update_students_list(DB_FILEPATH, all_students)

    if update_res:
        return {"message": f"{target_student.name} is now enrolled in {target_class.name}"}
    
    return {"message": f"Something went wrong"}